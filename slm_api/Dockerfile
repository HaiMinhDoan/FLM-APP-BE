FROM openlabs/docker-wkhtmltopdf:latest

# Cài đặt Python và pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean

# Cài đặt các phụ thuộc Python
WORKDIR /slm_api
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Cấu hình môi trường và lệnh khởi động
ENV XDG_RUNTIME_DIR=/tmp/runtime-root
EXPOSE 8080
CMD ["sh", "-c", "python3 -m app.init_db && uvicorn app.main:app --host 0.0.0.0 --port 8080"]
