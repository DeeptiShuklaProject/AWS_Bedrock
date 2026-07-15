#!/bin/bash
set -e

echo "=========================================="
echo "   AuraDocs Orchestrator & Launcher       "
echo "=========================================="

echo "1. Stopping existing containers..."
docker compose down

echo "2. Rebuilding and starting containers..."
docker compose up --build -d

echo "3. Waiting for services to initialize..."
sleep 4

echo "4. Container status:"
docker compose ps

echo "=========================================="
echo "AuraDocs is now running successfully!"
echo "👉 Open: http://localhost:8888"
echo "=========================================="
