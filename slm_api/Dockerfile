
FROM openlabs/docker-wkhtmltopdf:latest

# Cài đặt Python và pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# Copy requirements và cài đặt dependencies
WORKDIR /slm_api
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV XDG_RUNTIME_DIR=/tmp/runtime-root

EXPOSE 8080

# Chạy lệnh tạo bảng trước khi khởi động API
CMD ["sh", "-c", "python -m app.init_db && uvicorn app.main:app --host 0.0.0.0 --port 8080"]