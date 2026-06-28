# Dockerfile
FROM python:3.13-slim-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommands \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /School_Management_System

# Copy dependency files first (for caching)
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-cache

# Copy the rest of the code (excluding .env via .dockerignore)
COPY . .

# Set Python environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=school.settings \
    UV_VIRTUAL_ENV=/School_Management_System/.venv \
    PATH="/School_Management_System/.venv/bin:$PATH"

EXPOSE 8000

# Start Django (development)
CMD ["python", "school/manage.py", "runserver", "0.0.0.0:8000"]