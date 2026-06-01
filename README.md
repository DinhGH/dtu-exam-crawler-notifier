# Hệ thống tự động theo dõi và thông báo lịch thi (DTU) qua Email

## Mô tả

Dự án này xây dựng một hệ thống tự động thu thập dữ liệu từ website công bố lịch thi của Đại học Duy Tân (DTU) theo chu kỳ định kỳ (ví dụ: 1 giờ/lần). Hệ thống cho phép người dùng đăng ký theo dõi lịch thi bằng cách cung cấp mã/tên môn học, họ tên và địa chỉ email.

Khi hệ thống phát hiện một danh sách thi mới phù hợp với thông tin đăng ký của người dùng, nó sẽ tự động gửi một email thông báo chi tiết bao gồm ngày thi, phòng thi và các tệp đính kèm liên quan (nếu có).

## Tính năng chính

- **Tự động cào dữ liệu**: Hệ thống tự động truy cập và thu thập dữ liệu lịch thi từ website của DTU theo chu kỳ 1 giờ/lần.
- **Lưu trữ lịch thi**: Thu thập và lưu lại danh sách các tệp lịch thi mới được công bố.
- **Đăng ký theo dõi**: Người dùng có thể đăng ký nhận thông báo bằng cách cung cấp:
  - Mã hoặc tên môn học
  - Họ và tên
  - Địa chỉ email
- **Tìm kiếm tự động**: Hệ thống tự động quét các tệp lịch thi đã thu thập để tìm kiếm thông tin của sinh viên đã đăng ký.
- **Gửi Email thông báo**: Tự động gửi email đến người dùng khi phát hiện lịch thi phù hợp.
- **Tra cứu và Lọc dữ liệu**:
  - Hiển thị danh sách các tệp lịch thi đã được cào.
  - Hỗ trợ tìm kiếm và lọc dữ liệu theo thời gian hoặc số lượng tệp gần nhất.
  - Cho phép người dùng xem và tra cứu trực tiếp trên dữ liệu đã được hệ thống thu thập.
