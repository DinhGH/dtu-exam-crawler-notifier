# Hệ thống tự động theo dõi và thông báo lịch thi (DTU)

## Mô tả

Dự án này là hệ thống tự động thu thập dữ liệu lịch thi từ website Đại học Duy Tân (DTU). Hệ thống tự động cào dữ liệu định kỳ, lưu trữ, và thông báo qua Email khi có lịch thi phù hợp với người dùng đã đăng ký.

Dự án đã được triển khai (Live Demo): [https://dtu-exam-crawler-notifier-one.vercel.app/](https://dtu-exam-crawler-notifier-one.vercel.app/)

## Hướng dẫn cài đặt và chạy dự án

### 1. Yêu cầu hệ thống

- Python 3.10+
- Node.js 18+
- Git

### 2. Clone dự án

```bash
git clone https://github.com/DinhGH/dtu-exam-crawler-notifier.git
cd dtu-exam-crawler-notifier
```

### 3. Cài đặt và chạy Server (Backend)

```bash
cd server
# Tạo môi trường ảo (Virtual Environment)
python -m venv venv
# Kích hoạt môi trường
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Cài đặt thư viện
pip install -r requirements.txt

# Cấu hình biến môi trường
cp .env.example .env
# Mở file .env và điền các thông tin cấu hình (DATABASE_URL, EMAIL_SETTINGS, ...)

# Chạy server (Sử dụng lệnh sau từ thư mục 'server')
export PYTHONPATH=$PYTHONPATH:.
python -m uvicorn app.main:app --reload
```

### 4. Cài đặt và chạy Client (Frontend)

```bash
cd ../client
# Cài đặt thư viện
npm install

# Cấu hình biến môi trường
cp .env.example .env
# Mở file .env và cập nhật API_URL trỏ về server của bạn

# Chạy project
npm run dev
```

## Tính năng chính

- **Tự động cào dữ liệu**: Thu thập dữ liệu từ cổng thông tin lịch thi DTU.
- **Quản lý đăng ký**: Người dùng đăng ký môn học và nhận thông báo qua Email.
- **Tra cứu**: Giao diện dashboard hiện đại để tra cứu lịch thi và tình trạng đăng ký.
- **Thông báo**: Gửi email tự động khi có cập nhật mới.
