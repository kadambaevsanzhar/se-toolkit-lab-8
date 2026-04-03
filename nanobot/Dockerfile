# syntax=docker/dockerfile:1.7

FROM harbor.pg.innopolis.university/docker-hub-cache/python:3.14-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_LINK_MODE=copy
# Keep the venv outside /app/nanobot so docker-compose bind-mounts (./nanobot:/app/nanobot)
# do not hide the environment built in the image.
ENV UV_PROJECT_ENVIRONMENT=/opt/nanobot/.venv
ENV PATH="/root/.local/bin:${PATH}"
ENV PYTHONPATH="/app/nanobot:${PYTHONPATH}"

RUN apt-get update && apt-get install -y curl ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

WORKDIR /app

COPY --from=workspace /mcp /app/mcp
COPY --from=workspace /nanobot-websocket-channel /app/nanobot-websocket-channel
COPY . /app/nanobot

WORKDIR /app/nanobot
RUN /root/.local/bin/uv venv "${UV_PROJECT_ENVIRONMENT}"
RUN /root/.local/bin/uv sync

# nanobot-ai from PyPI does not register WebChat; lab uses nanobot-webchat on port 8765.
RUN /opt/nanobot/.venv/bin/python /app/nanobot/scripts/patch_channel_manager_webchat.py

# создаём бинарь nanobot вручную, если пакет не сгенерировал console script
RUN printf '%s\n' \
  '#!/opt/nanobot/.venv/bin/python' \
  'from nanobot.cli.commands import app' \
  'app()' \
  > /opt/nanobot/.venv/bin/nanobot \
  && chmod +x /opt/nanobot/.venv/bin/nanobot

FROM harbor.pg.innopolis.university/docker-hub-cache/python:3.14-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/nanobot/.venv/bin:${PATH}"

WORKDIR /app

RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid 1000 --create-home appuser

COPY --from=builder /app /app
COPY --from=builder /opt/nanobot /opt/nanobot

# a+rX: readable everywhere, execute only on dirs and already-exec files (fast; avoid +x on every .py in site-packages)
RUN chmod -R a+rX /app && \
    chmod -R a+rX /opt/nanobot

USER appuser

ENTRYPOINT ["python", "/app/nanobot/entrypoint.py"]
