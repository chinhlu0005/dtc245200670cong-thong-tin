# Sử dụng hình ảnh Python chính thức gọn nhẹ
FROM python:3.11-slim

# Thiết lập thư mục làm việc bên trong container
WORKDIR /app

# Copy file danh sách thư viện vào container
COPY requirements.txt .

# Cài đặt các thư viện Python
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn dự án vào container
COPY . .

# Mở cổng 8000 để truy cập web
EXPOSE 8000

# Lệnh khởi chạy ứng dụng khi container bắt đầu chạy
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]