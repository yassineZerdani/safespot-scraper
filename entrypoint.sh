#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "⏳ Waiting for the Core API (Django) to wake up..."

# Loop until the Django web container is accepting connections on port 8000
while ! nc -z web 8000; do
  sleep 2
done

echo "✅ Core API is online! Firing up the Playwright AI Scraper..."

# Execute the main command passed from the Dockerfile (python main.py)
exec "$@"