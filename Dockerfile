FROM python:3.12-slim
ARG NODE_VERSION=22

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends ripgrep curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

CMD ["mcp", "run", "mcp_server.py"]
