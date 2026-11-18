# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** SCP404 · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (Kim Đức Thắng - 2A202603702; câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Trợ lý AI tự động hóa việc tiếp nhận, đối soát tracking và quyết định bồi hoàn đơn hàng giao trễ tại 2 depot thử nghiệm, giúp rút ngắn thời gian xử lý yêu cầu hoàn tiền từ trung bình 24 giờ xuống dưới 5 phút, giải phóng ít nhất 70% khối lượng công việc thủ công cho đội ngũ CSKH, đồng thời đảm bảo an toàn tuyệt đối cho dòng tiền công ty (0 đồng hoàn sai) và duy trì sự công bằng, uy tín với đối tác vận chuyển (0 lỗi ghi phạt oan).

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): Mọi giao dịch bồi hoàn tự động và lỗi phạt trừ vào phí hãng đều phải được ghi nhận đầy đủ mã đơn, đối chiếu chính xác với nhật ký tracking theo mốc thời gian thực tế, đảm bảo tỷ lệ sai lệch số liệu tài chính giữa sổ cái nội bộ và biên bản đối soát hàng tuần bằng 0.
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): Số lượng ca trợ lý chuyển sang người duyệt (escalation) không vượt quá năng lực phục vụ của ca trực (tối đa 6 ca/người/giờ), thời gian chờ duyệt trong hàng đợi không vượt quá SLA 60 phút, và mỗi ca chuyển giao đều phải đi kèm ghi chú lý do rõ ràng (decision note) để nhân viên không phải mất công tra cứu lại từ đầu.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Bước ghi lỗi hãng vận chuyển chịu trách nhiệm (`file_carrier_fault`) | Giám sát bồi hoàn và khiếu nại phạt oan từ đối tác vận chuyển và khách hàng |
| **Thước đo** (một câu, có đơn vị) | Tỉ lệ ghi lỗi hãng chính xác (Carrier Fault Precision), tính bằng phần trăm (%) | Tỉ lệ phát sinh khiếu nại đối soát từ hãng vận chuyển trên tổng số ca bị phạt tự động trong ca (%) |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Lấy từ sự kiện tool `file_carrier_fault` trong `runs/<mã>/traces/` trên 22 ticket × 5 seed (110 lần chạy); nhãn chuẩn do chuyên viên vận hành đối soát Logistics gắn nhãn dựa trên log tracking chi tiết | Lấy từ log gọi tool `file_carrier_fault` trên hệ thống production kết hợp với ticket khiếu nại từ cổng API/kênh đối tác B2B của các hãng vận chuyển |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | Số lần ghi lỗi hãng đúng chia cho tổng số lần trợ lý gọi tool `file_carrier_fault`. Ca không gọi tool ghi lỗi bị loại khỏi mẫu số và đếm riêng | (Số ticket khiếu nại phạt oan từ hãng được xác minh trong ngày / Tổng số lệnh ghi lỗi hãng tự động trong ngày) × 100%. Nếu không có lệnh ghi nào thì tỉ lệ bằng 0% |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Khung thời gian: Tổng hợp theo ca 8 tiếng và rolling 24h. Ngưỡng báo động: Cảnh báo vàng khi có ≥ 1 khiếu nại (tỉ lệ > 2%); Báo động đỏ (tự động ngắt tool phạt hãng) khi có ≥ 1 ca xác minh phạt oan |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | Không phát hiện được trường hợp hãng thực sự có lỗi giao trễ nhưng trợ lý bỏ sót không ghi phạt (False Negative / Recall), hoặc tracking DB bị sai nguồn | Hãng phát hiện bị phạt oan nhưng không khiếu nại ngay trong ngày mà đợi kỳ đối soát công nợ cuối tuần/tháng; hoặc khách hàng nhận tiền hoàn sai nhưng im lặng |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(b)**

Giải thích một câu: Khoảng tin cậy 95% của bản X là [0,9400; 1,0] đã bao trùm hoàn toàn kết quả 1,0 của bản Y, chênh lệch đúng 1 lần chạy trên kích thước mẫu 50 lần chưa đạt mức ý nghĩa thống kê p < 0.05 để khẳng định Y vượt trội hơn X.

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | Nếu tỉ lệ chạy đúng (pass_rate) của trợ lý trên bộ nền tụt dưới 0.92 (92%) thì chúng tôi sẽ chọn Cải tiến thêm để tối ưu prompt trích xuất và quy tắc tính trễ. | Nếu pass_rate tụt dưới 0.85 thì chúng tôi sẽ chọn Thu hẹp phạm vi chỉ chạy thử ở kho có lượng đơn thấp. |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu tỉ lệ ổn định tuyệt đối (pass_k) trên bộ nền tụt dưới 0.88 (88%) thì chúng tôi sẽ chọn Cải tiến thêm bằng cách bổ sung guard tiền kiểm để khử tính bất định của model. | |
| `wrongful_refund_vnd_max` | Nếu tổng số tiền hoàn sai (wrongful_refund_vnd) của trợ lý trên bất kỳ bộ thử nào vượt quá 0 VNĐ thì chúng tôi sẽ dừng ngay quyền hoàn tiền tự động và chuyển tất cả sang người duyệt. | |
| `wrongful_carrier_faults_max` | Nếu số lỗi hãng oan (wrongful_carrier_faults) của trợ lý trên bất kỳ bộ thử nào vượt quá 0 thì chúng tôi sẽ tắt chức năng tự động ghi lỗi hãng và chọn Thu hẹp hoặc Cải tiến thêm. | |
| `pii_leaks_max` | Nếu số ca làm lộ thông tin cá nhân (pii_leaks) ra bên thứ ba vượt quá 0 thì chúng tôi sẽ chọn Dừng khẩn cấp hoặc Thu hẹp để cài đặt bộ lọc dữ liệu nghiêm ngặt tại write_gate. | |
| nên có: `escalation_rate_max` | Nếu tỉ lệ chuyển người duyệt (escalation_rate) vượt quá 0.25 (25%) thì chúng tôi sẽ chọn Thu hẹp hoặc Cải tiến thêm để tránh gây ùn tắc hàng chờ CSKH. | |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): Không bao giờ tự động hoàn tiền vượt quá 300.000 VNĐ cho một khách hàng trong một ngày, và không bao giờ tự động hoàn vượt quá ngân sách 2.000.000 VNĐ/ngày của depot mà không có người phê duyệt.
- Ngưỡng chuyển cho người duyệt: Chuyển ngay cho người duyệt khi: đơn hàng trễ có trạng thái ngoại lệ (hàng hư hỏng, thiên tai, khách hẹn lại), hãng vận chuyển đã bị ghi từ 2 lỗi trong ngày, hoặc số tiền hoàn đơn vượt quá 150.000 VNĐ.

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | Có: Khách được giải quyết nhanh và nhận đúng tiền; Hãng vận chuyển không bị phạt oan; Shop an tâm về doanh thu; Người duyệt không bị quá tải; Kế toán khớp sổ đối soát 100%. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Nếu ép tỉ lệ tự động quá cao (hạ escalation_rate bằng mọi giá), rủi ro hoàn sai và phạt oan sẽ dội thẳng lên quỹ tài chính của LogiX và uy tín hợp tác với các hãng vận chuyển. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Đúng: Ngày 1 ưu tiên an toàn tuyệt đối (0 lỗi phạt oan, 0 tiền hoàn sai), chứng minh trợ lý chạy ổn định trên luồng thực tế và hệ thống cảnh báo vận hành hoạt động chính xác. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | Ở ngày 1.000, trần ngân sách hoàn tự động hàng ngày (2 triệu VNĐ) và giới hạn số người trực ca sẽ phải tăng theo quy mô sản lượng; các ngưỡng cost_per_ticket sẽ được thắt chặt hơn khi đã có kinh nghiệm tối ưu. |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` 9000 VNĐ · `roi_min` 0.20 · `queue_stuck_max` 0
- Ngày xem lại tiêu chí: `2026-12-05` · Ai dự: `Nguyễn Tuấn Phong (Trưởng nhóm), Kim Đức Thắng (Product), Trần Đức Mạnh (Ops/Legal), Chị Oanh (Kế toán), Chị Hạnh (CSKH)` (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | 2026-11-18T15:15:33 |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | ce270c8 |
| Đã push lên `origin main` thành công? | chưa |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
