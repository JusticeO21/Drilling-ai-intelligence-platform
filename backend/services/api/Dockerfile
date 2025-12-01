FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    ENVIRONMENT=production \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --shell /bin/bash app

WORKDIR /app

COPY backend/common/requirements.txt /tmp/common-requirements.txt
RUN pip install --no-cache-dir -r /tmp/common-requirements.txt && \
    rm /tmp/common-requirements.txt

COPY backend/services/ai/requirements.txt /tmp/ai-requirements.txt
RUN pip install --no-cache-dir -r /tmp/ai-requirements.txt && \
    rm /tmp/ai-requirements.txt

COPY backend/services/api/requirements.txt /tmp/api-requirements.txt
RUN pip install --no-cache-dir -r /tmp/api-requirements.txt && \
    rm /tmp/api-requirements.txt

COPY backend/ ./

RUN mkdir -p /app/logs && \
    chown -R app:app /app

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "services.api.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
