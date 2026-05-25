FROM python:3.12-slim

# Install uv for fast dependency resolution
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Copy requirements and install deps
COPY requirements.txt .
RUN uv pip install --system -r requirements.txt

# Copy backend source code
COPY . .

# Expose port 8080 as requested
EXPOSE 8080

# Run FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
