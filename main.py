"""
Pipeline controller: RSS → scrape → AI extract → geocode → POST to Django.
"""
import asyncio
import os
import requests
from dotenv import load_dotenv
import feedparser

from scraper import scrape_url
from ai_extractor import extract_incident
from geocoder import geocode

load_dotenv()

RSS_URL = "https://news.google.com/rss/search?q=crime+OR+accident+OR+fire+Casablanca&hl=fr&gl=MA&ceid=MA:fr"
TOP_N = 5


def fetch_article_urls() -> list[str]:
    """Parse RSS and return top N article URLs."""
    feed = feedparser.parse(RSS_URL)
    urls = []
    for entry in feed.entries[:TOP_N]:
        link = entry.get("link")
        if link:
            urls.append(link)
    return urls


def push_to_django(payload: dict) -> bool:
    """POST payload to Django API. Returns True on success."""
    api_url = os.environ.get("DJANGO_API_URL")
    if not api_url:
        raise ValueError("DJANGO_API_URL not set")
    try:
        r = requests.post(api_url, json=payload, timeout=15)
        return r.status_code in (200, 201)
    except Exception:
        return False


async def process_url(url: str, title: str) -> None:
    """Scrape → extract → geocode → push. Skips on any failure."""
    try:
        text = await scrape_url(url)
        if not text:
            return
        incident = extract_incident(text)
        if not incident:
            return
        coords = geocode(incident.get("location", ""))
        if not coords:
            return
        lat, lng = coords
        payload = {
            "title": title,
            "incident_type": incident.get("incident_type", "other"),
            "severity_score": int(incident.get("severity_score", 50)),
            "lat": lat,
            "lng": lng,
            "source_url": url,
        }
        if push_to_django(payload):
            print(f"Pushed: {title[:50]}...")
    except Exception as e:
        print(f"Skip {url[:50]}...: {e}")


async def main():
    urls = fetch_article_urls()
    feed = feedparser.parse(RSS_URL)
    entries = feed.entries[:TOP_N]
    for i, url in enumerate(urls):
        title = entries[i].get("title", "Untitled") if i < len(entries) else "Untitled"
        await process_url(url, title)


if __name__ == "__main__":
    asyncio.run(main())
