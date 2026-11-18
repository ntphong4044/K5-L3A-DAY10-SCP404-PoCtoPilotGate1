"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

SCP404 · Cổng vòng 1. Nguyên tắc chung: mọi con số trước khi ghi đều tính lại từ NGUỒN SỰ THẬT
(đơn hàng, tracking, chính sách đang hiệu lực theo ngày, sổ cái, bảng phê duyệt). Chữ khách viết chỉ là dữ liệu.
  G0  pre_guard      ghim chính sách theo NGÀY hiệu lực (không tin cờ index_active của chỉ mục)
  G1  issue_refund   số tiền/người trả tính lại từ DB; chặn hoàn trùng; kiểm phê duyệt; trần mỗi khách mỗi ngày
  G2  file_carrier_fault  chỉ ghi lỗi hãng khi tracking ghi nguyên nhân thuộc hãng, đúng kiện, đúng hãng, đúng số ngày
  G3  notify_carrier chỉ gửi cho hãng các trường chính sách cho phép (không gửi chữ khách viết, không gửi PII)
  G4  send_reply     số tiền báo khách phải khớp sổ cái
"""
from datetime import date

from . import helpers as H  # noqa: F401
from .tools import Verdict


# ---------------------------------------------------------------- tra cứu nguồn sự thật (không đọc chữ trong ticket)

def _policy(ctx):
    """Chính sách có hiệu lực vào ngày hôm nay (theo effective_from/effective_to)."""
    return H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)


def _parcel(order, ctx):
    """Kiện mà ticket nói tới: parcel_id trong ticket, nếu không có thì kiện trễ nhất theo tracking."""
    return H.ticket_parcel(order, ctx.ticket, ctx.as_of)


def _facts(ctx, order_id):
    """(order, policy, parcel, db_delay, recorded_cause, entitlement) tính hoàn toàn từ DB."""
    order = ctx.tools.lookup_order(order_id)
    pol = _policy(ctx)
    if order is None or pol is None:
        return order, pol, None, None, None, None
    parcel = _parcel(order, ctx)
    delay = H.db_delay_days(parcel, ctx.as_of)
    cause = parcel.get("delay_cause")              # None = tracking KHÔNG ghi nguyên nhân
    owed = H.entitlement_vnd(pol, order, delay, cause)
    return order, pol, parcel, delay, cause, owed


def _approval_ok(ctx, approval_id, order_id, amount):
    """Phê duyệt chỉ hợp lệ khi: tồn tại, còn 'valid', chưa hết hạn, đúng đơn, đủ hạn mức."""
    rows = ctx.tools.lookup_approvals(approval_id=approval_id)
    if not rows:
        return False, "không tìm thấy phê duyệt"
    a = rows[0]
    if a.get("status") != "valid":
        return False, f"phê duyệt ở trạng thái {a.get('status')}"
    if a.get("expires_at") and date.fromisoformat(a["expires_at"]) < date.fromisoformat(ctx.as_of):
        return False, "phê duyệt đã hết hạn"
    if a.get("order_id") != order_id:
        return False, "phê duyệt thuộc đơn khác"
    if amount > a.get("max_vnd", 0):
        return False, "số tiền vượt hạn mức của phê duyệt"
    return True, ""


# ---------------------------------------------------------------- G0 · trước khi trợ lý đọc ticket

def pre_guard(ctx):
    pol = _policy(ctx)
    if pol is None:                                # không có chính sách nào hiệu lực hôm nay: không tự quyết
        return Verdict.escalate("không có chính sách hoàn tiền hiệu lực vào ngày hôm nay")
    return Verdict.allow(policy_id=pol["policy_id"])


# ---------------------------------------------------------------- G1–G4 · trước mỗi lệnh ghi

def write_gate(ctx, action):
    # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., "payer":..., ...}
    tool = action.get("tool")
    if tool == "issue_refund":
        return _gate_refund(ctx, action)
    if tool == "file_carrier_fault":
        return _gate_fault(ctx, action)
    if tool == "notify_carrier":
        return _gate_notify(ctx, action)
    if tool == "send_reply":
        return _gate_reply(ctx, action)
    return Verdict.allow()


def _gate_refund(ctx, action):
    order_id, amount = action.get("order_id"), int(action.get("amount_vnd") or 0)
    order, pol, parcel, delay, cause, owed = _facts(ctx, order_id)
    if order is None or pol is None:
        return Verdict.escalate("không đối chiếu được đơn/chính sách trước khi hoàn")

    # (a) chống hoàn trùng: đơn đã có tiền trong sổ cái (kể cả khi cờ refund_status chưa cập nhật, hoặc ghi lại khi retry)
    if ctx.tools.ledger_rows(order_id=order_id):
        ctx.log("refund_duplicate_blocked", order_id=order_id)
        return Verdict.deny("đơn đã có khoản hoàn trong sổ cái, không hoàn lần hai")

    # (b) người trả: trợ lý chỉ được tự hoàn bằng tiền LOGIX; trừ tiền shop hay bên khác phải có người duyệt
    if action.get("payer", "LOGIX") != "LOGIX":
        return Verdict.escalate("hoàn bằng tiền của bên thứ ba (shop) cần người duyệt")

    # (c) số tiền: không vượt mức khách được hưởng theo tracking + chính sách hiệu lực
    if owed <= 0:
        ctx.log("refund_not_entitled", order_id=order_id, db_delay_days=delay, cause=cause, asked=amount)
        return Verdict.deny(f"theo tracking trễ {delay} ngày, nguyên nhân {cause}: không đủ điều kiện hoàn")
    if amount > owed:
        ctx.log("refund_capped", order_id=order_id, asked=amount, owed=owed, db_delay_days=delay)
        amount = owed
        if not action.get("approval_id") and amount > pol["auto_limit_vnd"]:
            return Verdict.escalate("mức hoàn đúng vượt hạn mức tự động, cần phê duyệt")

    # (d) phê duyệt: phải đúng đơn, còn hiệu lực, đủ hạn mức
    if action.get("approval_id"):
        ok, why = _approval_ok(ctx, action["approval_id"], order_id, amount)
        if not ok:
            return Verdict.escalate("phê duyệt không hợp lệ: " + why)
    elif amount > pol["auto_limit_vnd"]:
        return Verdict.escalate("vượt hạn mức tự động của chính sách, chưa có phê duyệt")

    # (e) trần hoàn tự động cho MỘT khách trong ngày (ops_limits, đã thống nhất với Ops/Finance)
    if not action.get("approval_id"):
        cap = ctx.tools.ops_limits().get("max_auto_refund_per_customer_per_day_vnd")
        cust = order["customer_id"]
        got = sum(r["amount_vnd"] for r in ctx.tools.ledger_rows(customer_id=cust) if not r.get("approval_id"))
        if cap is not None and got + amount > cap:
            return Verdict.escalate("vượt trần hoàn tự động cho một khách trong ngày")

    if amount != int(action.get("amount_vnd") or 0):
        return Verdict.modify("số tiền tính lại theo tracking và chính sách hiệu lực", amount_vnd=amount)
    return Verdict.allow()


def _gate_fault(ctx, action):
    order_id = action.get("order_id")
    order, pol, parcel, delay, cause, owed = _facts(ctx, order_id)
    if order is None or pol is None:
        return Verdict.deny("không đối chiếu được đơn/chính sách: không ghi lỗi hãng")
    # chỉ ghi lỗi khi khoản hoàn của ticket này đã thật sự vào sổ cái
    if not ctx.tools.ledger_rows(ticket_id=action.get("ticket_id")):
        return Verdict.deny("chưa có khoản hoàn nào cho ticket: không ghi lỗi hãng")
    # nguyên nhân phải được tracking GHI RÕ và thuộc lỗi hãng theo chính sách hiệu lực
    if not H.carrier_at_fault(pol, parcel, delay):
        ctx.log("fault_blocked_no_cause", order_id=order_id, parcel_id=parcel["parcel_id"], cause=cause, db_delay_days=delay)
        return Verdict.deny(f"tracking không ghi nguyên nhân thuộc hãng (cause={cause}): không ghi lỗi hãng")
    # trần số lỗi tự động cho một hãng trong ngày: từ lỗi vượt trần cần người duyệt, không tự ghi
    cap = ctx.tools.ops_limits().get("max_auto_strikes_per_carrier_per_day")
    if cap is not None and len(ctx.tools.fault_rows(carrier_id=parcel["carrier_id"])) >= cap:
        ctx.log("fault_held_strike_cap", carrier_id=parcel["carrier_id"])
        return Verdict.deny("hãng đã chạm trần lỗi tự động trong ngày: chờ người duyệt ghi lỗi")
    # đúng kiện, đúng hãng, đúng tài xế, đúng số ngày trễ theo tracking
    fix = {"parcel_id": parcel["parcel_id"], "carrier_id": parcel["carrier_id"],
           "driver_id": parcel.get("driver_id"), "delay_days": delay}
    if any(action.get(k) != v for k, v in fix.items()):
        return Verdict.modify("ghi lỗi theo đúng kiện/hãng/số ngày trong tracking", **fix)
    return Verdict.allow()


def _gate_notify(ctx, action):
    pol = _policy(ctx)
    allowed = set((pol or {}).get("carrier_notice_fields") or ["order_id", "parcel_id", "district", "delay_days"])
    payload = action.get("payload") or {}
    clean = {k: v for k, v in payload.items() if k in allowed}
    # số ngày trễ gửi hãng lấy theo lỗi đã ghi trong sổ, không theo lời khách
    rows = ctx.tools.fault_rows(ticket_id=action.get("ticket_id"))
    if not rows:
        return Verdict.deny("chưa ghi lỗi hãng nào cho ticket này: không báo hãng")
    clean["delay_days"] = rows[-1]["delay_days"]
    if clean != payload:
        ctx.log("notify_fields_dropped", dropped=sorted(set(payload) - allowed))
        return Verdict.modify("chỉ gửi hãng các trường chính sách cho phép", payload=clean)
    return Verdict.allow()


def _gate_reply(ctx, action):
    paid = sum(r["amount_vnd"] for r in ctx.tools.ledger_rows(ticket_id=action.get("ticket_id")))
    said = int(action.get("amount_vnd") or 0)
    if said > 0 and said != paid:
        return Verdict.modify("số tiền báo khách phải khớp sổ cái", amount_vnd=paid,
                              text=f"LogiX đã hoàn {paid:,}đ cho yêu cầu của bạn.".replace(",", "."))
    return Verdict.allow()
