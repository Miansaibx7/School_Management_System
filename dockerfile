# Django Development Dockerfile Python + uv

FROM python:3.13-slim-bookworm

# Prevent Python from creating .pyc files and make output appear immediately.
# Set Python environment.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    DJANGO_SETTINGS_MODULE=school.settings \
    UV_VIRTUAL_ENV=/School_Management_System/.venv \
    PATH="/School_Management_System/.venv/bin:$PATH"

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv and uvx
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /School_Management_System

# Copy dependency files first — enables Docker layer caching so `uv sync`
# only re-runs when pyproject.toml/uv.lock actually change, not on every
# source-code edit
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-cache

# Copy the rest of the code (excluding .env via .dockerignore)
COPY . .

# Run as a non-root user. Running the app as root inside the
# container is unnecessary risk — if the app is ever compromised, root
# in the container is a much better foothold than a limited user.
RUN groupadd --system app && useradd --system --gid app --create-home app \
    && chown -R app:app /School_Management_System
USER app

EXPOSE 8000

# Container startup script — runs migrations / readiness checks before
# starting the dev server, rather than doing that inline in docker-compose's
# `command:` (keeps the image self-contained and runnable the same way
# in any environment, not just via that specific compose file)
COPY --chown=app:app docker-entrypoint.dev.sh /docker-entrypoint.dev.sh
RUN chmod +x /docker-entrypoint.dev.sh

ENTRYPOINT ["/docker-entrypoint.dev.sh"]