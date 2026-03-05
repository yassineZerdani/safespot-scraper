# Start with the same fast, slim Python image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# The Scraper Secret: We don't install map tools here. 
# We install the system dependencies required to run a headless Chromium browser.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        wget \
        gnupg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

# Install Python packages AND the Playwright browser binaries
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && playwright install --with-deps chromium

COPY . /app/

# We don't need a complex entrypoint.sh here. We just run the main python script.
CMD ["python", "main.py"]