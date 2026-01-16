FROM python:3.9-slim

WORKDIR /app

# Install system dependencies if needed (e.g. for numpy/pandas builds)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and models
COPY api/ api/
COPY models/ models/
# We intentionally do not copy data/ or notebooks/ to keep image small

# Expose the API port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
