# Use Python slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy only necessary files
COPY main.py .
COPY src/ ./src/
COPY examples/ ./examples/
COPY tests/ ./tests/

# Create non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Default command runs the demo
CMD ["python", "examples/demo.py"]