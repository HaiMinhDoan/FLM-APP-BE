# Sử dụng Python 3.13 làm base image
FROM python:3.13

FROM openlabs/docker-wkhtmltopdf:latest


# Copy requirements và cài đặt dependencies
WORKDIR /slm_api
COPY . /slm_api
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV XDG_RUNTIME_DIR=/tmp/runtime-root

EXPOSE 8080

# Chạy lệnh tạo bảng trước khi khởi động API
CMD ["sh", "-c", "python -m app.init_db && uvicorn app.main:app --host 0.0.0.0 --port 8080"]