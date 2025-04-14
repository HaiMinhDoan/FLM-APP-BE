# Sử dụng Python 3.10 làm base image
FROM python:3.13

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    libxrender1 libxext6 libfontconfig1 libjpeg62-turbo \
    xfonts-75dpi xfonts-base \
    && apt-get clean

# Cài đặt wkhtmltopdf có Qt patched
RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz \
    && tar xvf wkhtmltox*.tar.xz \
    && sudo mv wkhtmltox/bin/wkhtmlto* /usr/bin \
    && sudo apt-get install -y openssl build-essential libssl-dev libxrender-dev git-core libx11-dev libxext-dev libfontconfig1-dev libfreetype6-dev fontconfig

# Copy requirements và cài đặt dependencies
WORKDIR /slm_api
COPY . /slm_api
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV XDG_RUNTIME_DIR=/tmp/runtime-root

EXPOSE 8080

# Chạy lệnh tạo bảng trước khi khởi động API
CMD ["sh", "-c", "python -m app.init_db && uvicorn app.main:app --host 0.0.0.0 --port 8080"]