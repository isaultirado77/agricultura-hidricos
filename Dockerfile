# Base
FROM python:3.12-slim AS base

WORKDIR /app

# Copy dependency files 
COPY ["pyproject.toml", "uv.lock", "/app/"]

# Install uv
RUN pip install --no-cache-dir uv

# Install deps
RUN uv sync --frozen

# Copy rest of the project
COPY . .
