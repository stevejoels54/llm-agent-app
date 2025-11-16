FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY utils/ ./utils/
COPY static/ ./static/

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Use port 8080 (non-privileged) instead of 80 - non-root users can't bind to ports < 1024
EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "main:app"]
