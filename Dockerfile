FROM python:3.11-slim

LABEL maintainer="Team Albania"
LABEL description="EagleFarm - Attack/Defense CTF Exploit Farm"

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server/ ./server/

RUN mkdir -p /app/data /app/logs

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

CMD ["python", "-m", "server.app"]