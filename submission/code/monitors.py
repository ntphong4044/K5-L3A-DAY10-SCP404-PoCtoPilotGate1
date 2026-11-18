"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def _has(t, event_type, **kw):
    return any(e.get("type") == event_type and all(e.get(k) == v for k, v in kw.items()) for e in t.get("events") or [])


def claim_override_rate(trials):
    """Kỹ thuật: tỉ lệ ticket mà model đè số ngày trễ khách tự khai lên số ngày trong tracking DB."""
    return sum(_has(t, "model_override") for t in trials) / max(1, len(trials))


def gate_intervention_rate(trials):
    """Kỹ thuật/pháp lý: tỉ lệ ticket mà cổng phải chặn, sửa hoặc chuyển người ở một lệnh ghi
    (gate của bàn, cổng pháp lý trong config, hoặc luật phía host). Tăng vọt = trợ lý đang đề xuất sai nhiều hơn."""
    kinds = ("gate", "legal_gate", "host_denied", "business_gate")
    return sum(any(e.get("type") in kinds for e in t.get("events") or []) for t in trials) / max(1, len(trials))


def llm_degraded_rate(trials):
    """Vận hành: tỉ lệ ticket gặp lỗi LLM (429, fallback, ghi lại khi không chắc) — báo trước giờ cao điểm."""
    kinds = ("llm_error", "llm_fallback", "write_retry")
    return sum(any(e.get("type") in kinds for e in t.get("events") or []) for t in trials) / max(1, len(trials))


def tracking_incomplete_rate(trials):
    """Tỉ lệ ticket bị giữ vì tracking thiếu/mâu thuẫn; không dùng nhãn chấm."""
    return sum(_has(t, "guard", kind="tracking_incomplete") for t in trials) / max(1, len(trials))


def refund_underpayment_held_rate(trials):
    """Tỉ lệ ticket cổng phát hiện đề xuất hoàn thiếu hoặc từ chối sai quyền lợi."""
    return sum(_has(t, "guard", kind="refund_underpayment_held") for t in trials) / max(1, len(trials))


def carrier_strike_cap_held_rate(trials):
    """Tỉ lệ ticket bị giữ lệnh ghi lỗi hãng do chạm trần tự động trong ngày."""
    return sum(_has(t, "guard", kind="fault_held_strike_cap") for t in trials) / max(1, len(trials))


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "claim_override_rate": claim_override_rate,
    "gate_intervention_rate": gate_intervention_rate,
    "llm_degraded_rate": llm_degraded_rate,
    "tracking_incomplete_rate": tracking_incomplete_rate,
    "refund_underpayment_held_rate": refund_underpayment_held_rate,
    "carrier_strike_cap_held_rate": carrier_strike_cap_held_rate,
}
STARTER_MONITORS = ("escalation_rate",)
