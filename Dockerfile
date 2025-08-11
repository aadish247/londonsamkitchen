FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required for numpy and pandas
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with specific versions to avoid compatibility issues
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir numpy==1.24.3 && \
    pip install --no-cache-dir pandas==2.0.3 && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create the instance directory for SQLite database
RUN mkdir -p instance

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

# Expose the port the app runs on
EXPOSE 8080

# Add entrypoint script and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Command to run the application
CMD ["/entrypoint.sh"]