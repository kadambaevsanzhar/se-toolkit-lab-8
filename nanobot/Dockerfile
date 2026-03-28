# syntax=docker/dockerfile:1.7

FROM python:3.14-slim-bookworm AS builder

ARG APP_UID=1000
ARG APP_GID=1000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app/nanobot
COPY --from=workspace /mcp /app/mcp
COPY --from=workspace /nanobot-websocket-channel /app/nanobot-websocket-channel

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

RUN python -m ensurepip --upgrade
RUN python -m pip install --upgrade pip setuptools wheel

# CLI nanobot
RUN python -m pip install "nanobot-ai>=0.1.4.post6"

# LMS MCP project lives at /app/mcp
RUN python -m pip install -e /app/mcp

# Webchat plugin + Webchat MCP
# сначала protocol
RUN python -m pip install -e /app/nanobot-websocket-channel/nanobot-channel-protocol

# потом webchat
RUN python -m pip install -e /app/nanobot-websocket-channel/nanobot-webchat

# потом mcp-webchat
RUN python -m pip install -e /app/nanobot-websocket-channel/mcp-webchat

FROM python:3.14-slim-bookworm AS runtime

ARG APP_UID=1000
ARG APP_GID=1000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:${PATH}"

WORKDIR /app

RUN groupadd --gid "${APP_GID}" appgroup \
    && useradd --uid "${APP_UID}" --gid "${APP_GID}" --create-home --shell /bin/bash appuser

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder --chown=${APP_UID}:${APP_GID} /app /app

USER appuser

CMD ["python", "/app/nanobot/entrypoint.py"]
