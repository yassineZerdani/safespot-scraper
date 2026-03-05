FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Added netcat-openbsd so the entrypoint can ping the Django API
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        wget \
        gnupg \
        netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && playwright install --with-deps chromium

COPY . /app/

# Strip Windows line endings and make the entrypoint executable
RUN sed -i 's/\r$//' /app/entrypoint.sh \
    && chmod +x /app/entrypoint.sh

# Set the entrypoint to handle startup logic
ENTRYPOINT ["/app/entrypoint.sh"]

# The default command that gets passed to the entrypoint
CMD ["python", "main.py"]