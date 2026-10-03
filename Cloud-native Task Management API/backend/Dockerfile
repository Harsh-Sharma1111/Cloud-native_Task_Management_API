# Stage 1: Build stage
FROM python:3.11-slim AS builder

WORKDIR /build

# Create a virtual environment
RUN python -m venv /opt/venv

# Ensure all pip commands use the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install dependencies
# We also install gunicorn here since it's required for the entrypoint
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt gunicorn

# Stage 2: Runtime stage
FROM python:3.11-slim

# Create a non-root user and group
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder --chown=appuser:appgroup /opt/venv /opt/venv

# Set path to use the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy the rest of the application code
COPY --chown=appuser:appgroup . .

# Switch to the non-root user
USER appuser

# Expose the application port
EXPOSE 5000

# Start the application using gunicorn
# Adjusted from "run:create_app()" to use the "app" object defined in run.py
CMD ["gunicorn", "--workers", "4", "--timeout", "30", "--bind", "0.0.0.0:5000", "run:app"]
