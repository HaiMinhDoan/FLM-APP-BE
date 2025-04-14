
FROM openlabs/docker-wkhtmltopdf:latest
# Sử dụng Python 3.13 làm base image
FROM python:3.13 as python-base

# Cài đặt pip nếu chưa có
RUN apt-get update && apt-get install -y python3-pip

# Copy requirements và cài đặt dependencies
WORKDIR /slm_api
COPY . .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV XDG_RUNTIME_DIR=/tmp/runtime-root

EXPOSE 8080

# Chạy lệnh tạo bảng trước khi khởi động API
CMD ["sh", "-c", "python -m app.init_db && uvicorn app.main:app --host 0.0.0.0 --port 8080"]