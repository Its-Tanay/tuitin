# Use Python slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py .
COPY src/ ./src/
COPY data/ ./data/
COPY examples/ ./examples/
COPY tests/ ./tests/

# Create non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Default command runs the demo
CMD ["python", "examples/demo.py"]