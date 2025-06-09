FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
      && rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
WORKDIR /app

COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

ENV APP_CONFIG=configs/app.yaml

# Default command
CMD ["bash"]