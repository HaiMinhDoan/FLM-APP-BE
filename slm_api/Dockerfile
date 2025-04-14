
# Sử dụng Python 3.13 làm base image
FROM python:3.13


RUN apt-get update && \
    apt-get install -y wget xfonts-75dpi xfonts-base && \
    wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb && \
    dpkg -i wkhtmltox_0.12.6-1.focal_amd64.deb || apt-get -fy install && \
    rm wkhtmltox_0.12.6-1.focal_amd64.deb


# Copy requirements và cài đặt dependencies
WORKDIR /slm_api
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV XDG_RUNTIME_DIR=/tmp/runtime-root

EXPOSE 8080

# Chạy lệnh tạo bảng trước khi khởi động API
CMD ["sh", "-c", "python -m app.init_db && uvicorn app.main:app --host 0.0.0.0 --port 8080"]