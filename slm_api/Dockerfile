
# Sử dụng Python 3.13 làm base image
FROM python:3.13 as python-base


# Cài đặt các phụ thuộc cần thiết
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    libfontconfig1 \
    libjpeg62-turbo \
    libpng16-16 \
    libx11-6 \
    libxext6 \
    libxrender1 \
    xfonts-75dpi \
    xfonts-base \
    qtbase5-dev \
    qtchooser \
    qt5-qmake \
    qtbase5-dev-tools \
    wget \
    ca-certificates && \
    apt-get clean

# Tải và biên dịch wkhtmltopdf
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox-0.12.6.1-3.almalinux8.aarch64.rpm && \
    dpkg -i wkhtmltox-0.12.6.1-3.almalinux8.aarch64.rpm && \
    apt-get install -f && \
    rm wkhtmltox-0.12.6.1-3.almalinux8.aarch64.rpm


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