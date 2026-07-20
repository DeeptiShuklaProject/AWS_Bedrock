FROM python:3.11-slim

# Install OpenJDK 17, Go, and Node.js for multi-language execution support
RUN apt-get update && \
    apt-get install -y --no-install-recommends default-jdk-headless golang-go nodejs && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install pip dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
