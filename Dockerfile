# Base
FROM python:3.12-slim AS base

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock


# Install uv 
RUN pip install --no-cache-dir uv

# Install deps
RUN uv sync --frozen

# Copy rest of code
COPY . .

# Create project directories
RUN mkdir -p data/raw data/processed data/interim data/temp log

# Default command 
CMD ["uv", "run", "python", "-m", "main"]
