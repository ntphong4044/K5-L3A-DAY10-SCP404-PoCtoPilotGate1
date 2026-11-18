# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): SCP404
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-SCP404-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8):

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

Tham gia phân tích log và thiết kế các hàm tiền kiểm và hậu kiểm cho các hành động ghi.

### Bằng chứng

...

### Exit ticket

Một điều học được: Sự khác biệt giữa can thiệp prompt model và dựng rào chắn cấp hệ thống bằng code.
Một điều còn chưa chắc: Cách kiểm soát các lỗi chìm không phát hiện qua test công khai.

## KimDucThang-2A202603702

### Phần việc phụ trách

Vai: Sản phẩm và kinh doanh. Phụ trách Bản tiêu chí chấp nhận (Phiếu A, `config/acceptance_criteria.json`), bản đồ dữ liệu, cổng kinh doanh (`config/operating_gates.json`), tính toán chi phí và ROI, dự thảo quyết định Gate 1.

### Đóng góp cụ thể

Xây dựng bộ chỉ số chấp nhận, xác định ngưỡng chi phí tối đa và ROI tối thiểu từ `ops_facts`.

### Bằng chứng

...

### Exit ticket

Một điều học được: Không được thay đổi tiêu chí chấp nhận sau khi đã quan sát dữ liệu đánh giá.
Một điều còn chưa chắc: Dự báo độ trôi dạt dữ liệu (data drift) chính xác khi mở rộng quy mô pilot.

## TranDucManh-2A202603615

### Phần việc phụ trách

Vai: Vận hành và pháp lý. Phụ trách phân tích HAZOP mở rộng ngoài kỹ thuật, checklist 9 nhóm việc, cổng vận hành và pháp lý (`config/operating_gates.json`), kịch bản vận hành (runbook).

### Đóng góp cụ thể

Rà soát các nguy cơ về nhân sự duyệt, thời gian hàng chờ và bảo mật dữ liệu PII trước khi gửi cho đối tác vận chuyển.

### Bằng chứng

...

### Exit ticket

Một điều học được: Cổng an toàn không chỉ nằm ở code mà còn ở quy trình vận hành và phân công con người.
Một điều còn chưa chắc: Năng lực xử lý thực tế của nhân viên chăm sóc khách hàng trong các khung giờ cao điểm đột biến.
