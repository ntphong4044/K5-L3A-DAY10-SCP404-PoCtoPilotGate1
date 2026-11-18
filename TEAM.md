# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): SCP404
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-SCP404-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): S1

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Nguyễn Tuấn Phong | 2A202603712 | Kỹ sư cổng | x |
|   2 | Lê Anh Quân | 2A202603576 | Kỹ sư cổng | |
|   3 | Kim Đức Thắng | 2A202603702 | Sản phẩm và kinh doanh | |
|   4 | Trần Đức Mạnh | 2A202603615 | Vận hành và pháp lý | |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## NguyenTuanPhong-2A202603712

### Phần việc phụ trách

Vai: Kỹ sư cổng (trưởng nhóm). Phụ trách chạy mốc base, chuẩn bị và chốt cổng vòng 1 (`lab10/guards.py`), điều phối kỹ thuật và quản lý repository.

### Đóng góp cụ thể

Khởi tạo repository, cấu hình remote `origin` và `upstream`, thiết lập git identity, chạy kiểm tra public test ban đầu đạt 13/13 tests.

### Bằng chứng

`git remote -v`, `Ran 13 tests … OK`.

### Exit ticket

Một điều học được: Tầm quan trọng của việc chốt cổng và ký tiêu chí trước khi chạy eval.
Một điều còn chưa chắc: Cách tối ưu hóa cân bằng giữa tỉ lệ chuyển người duyệt và chi phí vận hành.

## LeAnhQuan-2A202603576

### Phần việc phụ trách

Vai: Kỹ sư cổng. Phụ trách trace các ca lỗi, behavioral test, thiết kế logic chặn trong `lab10/guards.py` và theo dõi trong `lab10/monitors.py`.

### Đóng góp cụ thể

Hoàn thiện CP4 thẻ S1: phân tích khai tăng/giảm ngày trễ, tracking đã giao nhưng thiếu ngày, trần lỗi hãng cùng ngày. Bổ sung tiền kiểm tracking, cổng giữ đề xuất hoàn thiếu/từ chối sai và ba monitor; điền Phiếu C0–C11, cập nhật runbook và bàn giao CP5. Có dùng Codex hỗ trợ đọc trace, sửa code, chạy kiểm tra và soạn tài liệu; cần tự nắm logic và con số để giải thích lúc demo.

### Bằng chứng

Grade `R-S1-grade-20261118-163851-5c9f7b`: PASS-VISIBLE; integrity, criteria, visible, regression, monitor đều đạt. S1 đúng 65/65 lượt, base 110/110; 13/13 test công khai qua. Phiếu C0–C11 và `docs/CP4-S1-handoff.md`; report lưu trong `submission/cp4-evidence/` để bàn giao qua Git.

### Exit ticket

Một điều học được: Cổng chỉ kiểm lệnh hoàn chưa đủ; khách khai thấp có thể làm agent từ chối trước khi gọi lệnh, nên phải kiểm cả đường gửi kết luận. Tracking là nguồn sự thật nhưng vẫn phải kiểm tính đầy đủ.
Một điều còn chưa chắc: Tỉ lệ timestamp hợp lệ nhưng sai, lỗi tích luỹ 7 ngày và chất lượng xử lý tay trong pilot thật; PASS-VISIBLE chưa chứng minh qua test ẩn.

## KimDucThang-2A202603702

### Phần việc phụ trách

Vai: Sản phẩm và kinh doanh. Phụ trách Bản tiêu chí chấp nhận (Phiếu A, `config/acceptance_criteria.json`), bản đồ dữ liệu, cổng kinh doanh (`config/operating_gates.json`), tính toán chi phí và ROI, dự thảo quyết định Gate 1.

### Đóng góp cụ thể

Xây dựng bộ chỉ số chấp nhận trong `config/acceptance_criteria.json`, xác định ngưỡng chi phí tối đa (9.000đ) và ROI tối thiểu (0.20) từ `ops_facts`, điền Phiếu A và cổng kinh doanh trong `config/operating_gates.json`, phân tích cơ cấu chi phí theo từng kho và tham gia dự thảo quyết định v1, v2.

### Bằng chứng

Bản tiêu chí chấp nhận đã ký và khóa hash `47bfef52`, Phiếu A đầy đủ các mục, cổng kinh doanh `business` trong `config/operating_gates.json`, các chỉ số chi phí và ROI trên report ba mốc.

### Exit ticket

Một điều học được: Không được thay đổi tiêu chí chấp nhận sau khi đã quan sát dữ liệu đánh giá.
Một điều còn chưa chắc: Dự báo độ trôi dạt dữ liệu (data drift) chính xác khi mở rộng quy mô pilot.

## TranDucManh-2A202603615

### Phần việc phụ trách

Vai: Vận hành và pháp lý. Phụ trách phân tích HAZOP mở rộng ngoài kỹ thuật, checklist 9 nhóm việc, cổng vận hành và pháp lý (`config/operating_gates.json`), kịch bản vận hành (runbook), hoàn tất thẩm định và thủ tục bàn giao CP5.

### Đóng góp cụ thể

Rà soát các nguy cơ về nhân sự duyệt, thời gian hàng chờ và bảo mật dữ liệu PII trước khi gửi cho đối tác vận chuyển; điền cổng `operations` và `legal`, hoàn thiện Runbook 1–5, soát toàn bộ Phiếu C (C0–C11), chốt quyết định Gate 1 v2 tại C12, hoàn thiện `submission/submission.json` và thu thập gói bài nộp CP5 đạt trạng thái ĐỦ THÀNH PHẦN.

### Bằng chứng

Phiếu B mục B4–B5, B7.5–B7.6; Phiếu C mục C11–C12; `submission/submission.json`; lệnh `check_submission` in `ĐỦ THÀNH PHẦN`; report tự kiểm tra `R-S1-grade-20261118-171024-5a0d66` đạt PASS-VISIBLE.

### Exit ticket

Một điều học được: Cổng an toàn không chỉ nằm ở code mà còn ở quy trình vận hành và phân công con người.
Một điều còn chưa chắc: Năng lực xử lý thực tế của nhân viên chăm sóc khách hàng trong các khung giờ cao điểm đột biến.
