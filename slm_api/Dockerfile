# Sử dụng Python 3.10 làm base image
FROM python:3.13

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    libxrender1 libxext6 libfontconfig1 libjpeg62-turbo \
    xfonts-75dpi xfonts-base \
    && apt-get clean

# Cài đặt wkhtmltopdf có Qt patched
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.bookworm_amd64.deb \
    && dpkg -i wkhtmltox_0.12.6-1.bookworm_amd64.deb \
    && rm wkhtmltox_0.12.6-1.bookworm_amd64.deb

# Copy requirements và cài đặt dependencies
WORKDIR /slm_api
COPY . /slm_api
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV XDG_RUNTIME_DIR=/tmp/runtime-root

EXPOSE 8080

# Chạy lệnh tạo bảng trước khi khởi động API
CMD ["sh", "-c", "python -m app.init_db && uvicorn app.main:app --host 0.0.0.0 --port 8080"]