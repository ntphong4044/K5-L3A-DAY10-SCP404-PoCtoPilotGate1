# Bàn giao CP4 S1 cho CP5

Người thực hiện CP4: Lê Anh Quân, có Codex hỗ trợ. Người nhận phần CP5: Trần Đức Mạnh. Ngày 2026-11-18 (GMT+7). Bản bàn giao và bằng chứng được lưu cùng commit CP4; Mạnh kéo `origin main` để nhận trước khi làm CP5.

## Kết quả CP4

- Phiếu C0–C11 đã điền; C12 giữ nguyên để Mạnh quyết v2.
- `lab10/guards.py`: tiền kiểm tracking thiếu/mâu thuẫn trước khi tính trễ; chuyển người nếu đề xuất hoàn dương bị thiếu hoặc từ chối sai quyền lợi. Giữ cổng CP3, trần 2 lỗi tự động/hãng/ngày, không xử lý riêng theo mã ticket/câu chữ.
- `lab10/monitors.py`: thêm `tracking_incomplete_rate`, `refund_underpayment_held_rate`, `carrier_strike_cap_held_rate`.
- Config vận hành không đổi: 4 kho lẻ, 1 người × 6 ca/giờ, kiểm mẫu 10%, decision_note bật. Không có bằng chứng từ S1 cần tăng người thường trực.
- Gói S1–S8 đã đủ và khớp manifest; chỉ đọc/phân tích S1. `.gitattributes` ghim LF để clone Windows không đổi byte các file khóa. Tiêu chí và bản chốt vòng 1 khớp hash gốc.

| Chỉ số S1 | base | prepared | after |
|---|---:|---:|---:|
| pass_rate / pass_k | 0.3077 / 0.3077 | 0.7692 / 0.7692 | 1.0 / 1.0 |
| Hoàn sai, tổng 5 seed | 985.000đ | 275.000đ | 0đ |
| Hoàn thiếu, tổng 5 seed | 105.000đ | 105.000đ | 0đ |
| Lỗi hãng oan, tổng 5 seed | 30 | 5 | 0 |
| PII | 0 | 0 | 0 |
| Chi phí/ticket | 2.964đ | 3.656đ | 5.870đ |
| ROI | -2.74 | 0.58 | 0.70 |
| Escalation / tổng tỉ lệ vào review | 0 / 0 | 0 / 0.1538 | 0.2308 / 0.3846 |

After S1 đúng 65/65 trial; base đúng 110/110, 4.456đ/ticket, ROI 1.24. Cả hai bộ coverage 1.0, hàng chờ không ùn, chờ tối đa 0 phút, không vượt trần. 13/13 test công khai qua. Các số ngày/chi phí là mô phỏng, chưa phải pilot thật.

Grade cuối: `R-S1-grade-20261118-163851-5c9f7b`, **PASS-VISIBLE (chưa chạy test ẩn)**. Integrity, criteria, visible, regression, monitor đều xanh. Hash code `5c9f7b09b966`; hash vòng 1 `17ece2bb`; tiêu chí `47bfef52`. Ba mốc của grade:

- base: `R-S1-before-20261118-163851-5c9f7b`
- prepared: `R-S1-prepared-20261118-163851-5c9f7b`
- after: `R-S1-after-20261118-163851-5c9f7b`

Report và nhật ký được sao lưu trong `submission/cp4-evidence/`; `runs/` bị Git bỏ qua. Grade đầu có integrity đỏ do chưa nhận đủ gói, bản cuối đã giải quyết. Không dùng bản thử cô lập `b0aec9` làm bản bàn giao; code cuối là `5c9f7b`.

## Việc Mạnh làm ở CP5

1. Đọc C0–C11, soát runbook, xác nhận đúng PIC. Ghi tên/ngày khi thực sự soát; chưa ghi nhận Mạnh đã soát thay bạn. Đặc biệt: lệnh fault bị giữ do cap không tự tạo queue riêng trong mock; NV-OANH phải rà event trong ngày. Cổng ngày chưa bao phủ cửa sổ lỗi 7 ngày của hãng.
2. Điền C12: so v1 với v2, ba bằng chứng và ba dòng bắt buộc. Report ghi mọi ngưỡng đã ký đều đạt và “được phép cân nhắc Tiếp tục”; quyết định cuối và chữ ký thuộc nhóm. Phân khúc S1 đắt nhất là CT 7.053đ/ticket, vẫn đạt; ở base nhóm đơn không xác định `?` 10.359đ/ticket do phải xử lý tay. Nêu rõ phần chưa đo: tracking thật, POD, tải sale, duyệt tay, test ẩn và lỗi 7 ngày.
3. Điền `submission/submission.json`: team đúng tiêu chí, incident S1, decision_v1/v2, ba câu chép từ C12. Members theo `TEAM.md`: `NguyenTuanPhong-2A202603712`, `LeAnhQuan-2A202603576`, `KimDucThang-2A202603702`, `TranDucManh-2A202603615`.
4. Trên máy nhận bàn giao, chạy lại grade để sinh thư mục runs tại máy đó, rồi collect. Nếu demo sửa config thì hoàn nguyên bản v2 và chạy lại hai lệnh. Không chép report cũ rồi coi là đã chạy trên code mới.

```powershell
python -m lab10.checkpoint verify
python -m lab10.criteria verify
python -m lab10.grade --incident S1
python -m lab10.check_submission --collect
```

Chỉ chốt khi collector in `ĐỦ THÀNH PHẦN`. Mỗi người tự xác nhận mục cá nhân/exit ticket và nộp link LMS. Sau CP5 commit/push bài cuối theo README. Chưa gửi tin hay thông báo nào cho Mạnh/hãng từ phiên này.

## Điểm cần giải thích khi demo

- S1-01: lời khách 5 ngày so DB 2; cổng CP3 đã chặn.
- S1-20/21: DELIVERED nhưng thiếu ngày giao; cổng CP4 chuyển người trước khi ghi tiền/lỗi, không lấy hôm nay làm ngày giao.
- S1-07: lời khách 2 so DB 4; agent định từ chối, cổng CP4 chuyển người. Pass ở ca này nghĩa là chuyển người đúng, chưa phải tự hoàn xong.
- S1-40…43: cap 2 giới hạn lỗi tự động nhưng vẫn phục vụ khoản hoàn hợp lệ. Cap chỉ giới hạn thiệt hại; không chứng minh lỗi dưới cap đúng hoặc xử lý hết lịch sử 7 ngày.

Trong sandbox có thể xuất hiện cảnh báo Git “chưa thấy commit khóa” do khác chủ sở hữu workspace; lịch sử thực có commit `ce270c8`. Không ký lại tiêu chí. Trên máy chính chủ dùng `git log --oneline -- config/acceptance_criteria.lock` để đối chiếu.
