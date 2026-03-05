# SafeSpot AI Scraper

Standalone Python microservice that scrapes news, extracts incident data with Gemini AI, geocodes locations, and pushes to the Django API.

## Setup

```bash
cd safespot-ai-scraper
python3 -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
playwright install chromium
```

## Configuration

Copy `.env.example` to `.env` and set:

- `GEMINI_API_KEY` – Your Google AI API key
- `DJANGO_API_URL` – e.g. `http://localhost:8000/api/incidents/`

## Run

```bash
python main.py
```

## Docker

```bash
docker build -t safespot-scraper .
docker run --env-file .env safespot-scraper
```

## Django

Ensure the incidents API is running and migrations are applied:

```bash
cd ../core
python manage.py makemigrations incidents
python manage.py migrate
python manage.py runserver
```
