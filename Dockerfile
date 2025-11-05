FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN mkdir -p /root/.pip && \
    echo "[global]" > /root/.pip/pip.conf && \
    echo "index-url = https://pypi.mirrors.ustc.edu.cn/simple/" >> /root/.pip/pip.conf

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install system dependencies required by Playwright browsers.
RUN playwright install-deps

COPY . .

# Ensure Chromium browser binaries are available inside the container.
ENV PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright
RUN python -m playwright install --with-deps chromium

EXPOSE 6424

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6424"]
