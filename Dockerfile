FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data/payments data/quiz_history data/plans

# Environment variables
ENV ENVIRONMENT=production
ENV GEMINI_API_KEY=""
ENV TELEGRAM_BOT_TOKEN=""
ENV JWT_SECRET=""
ENV SECRET_KEY=""

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/readyz || exit 1

# Run with production settings
CMD ["python", "run_backend.py"]
