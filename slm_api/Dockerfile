
# Sử dụng Python 3.13 làm base image
FROM python:3.13 as python-base


# Cài đặt các phụ thuộc hệ thống cần thiết cho wkhtmltopdf và các thư viện hỗ trợ
RUN apt-get update && \
    apt-get install -y \
    wget \
    xfonts-75dpi \
    xfonts-base \
    fontconfig \
    libjpeg62-turbo \
    libxrender1 \
    libxext6 \
    libssl3 \
    ca-certificates \
    libfontconfig1 \
    libx11-6 && \
    apt-get clean

# Tải và cài đặt wkhtmltopdf with patched qt
RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.6/wkhtmltox_0.12.6-1.bionic_amd64.deb && \
    dpkg -i wkhtmltox_0.12.6-1.bionic_amd64.deb && \
    apt-get install -f && \
    rm wkhtmltox_0.12.6-1.bionic_amd64.deb


# Cài đặt pip nếu chưa có
RUN apt-get update && apt-get install -y python3-pip

# Copy requirements và cài đặt dependencies
WORKDIR /slm_api
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV XDG_RUNTIME_DIR=/tmp/runtime-root

EXPOSE 8080

# Chạy lệnh tạo bảng trước khi khởi động API
CMD ["sh", "-c", "python -m app.init_db && uvicorn app.main:app --host 0.0.0.0 --port 8080"]