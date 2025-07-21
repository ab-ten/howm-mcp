FROM python:3.12-slim AS base

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends ripgrep curl \
    && rm -rf /var/lib/apt/lists/*

COPY src/requirements/requirements.txt /tmp/requirements.txt
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt


FROM base AS runtime
CMD ["mcp", "run", "mcp_server.py"]


FROM base AS dev
COPY src/requirements/requirements-dev.txt /tmp/requirements-dev.txt
RUN pip install --no-cache-dir -r /tmp/requirements-dev.txt \
    && rm /tmp/requirements-dev.txt
