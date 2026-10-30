FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev libpango-1.0-0 libpangoft2-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY . .
RUN pip install --no-cache-dir -e ".[dev]"

EXPOSE 8000
CMD ["gunicorn", "config.asgi:application", "--bind", "0.0.0.0:8000", \
     "--workers", "3", "--worker-class", "uvicorn.workers.UvicornWorker"]
