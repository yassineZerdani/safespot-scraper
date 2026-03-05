"""
Scraper module: fetches page content using Playwright (headless Chromium).
"""
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


async def scrape_url(url: str, timeout_ms: int = 30000) -> str | None:
    """
    Open URL in headless Chromium, wait for network idle, extract all <p> text.
    Returns concatenated paragraph text or None on failure.
    """
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            page = await context.new_page()
            await page.goto(url, wait_until="networkidle", timeout=timeout_ms)
            html = await page.content()
            await browser.close()

        soup = BeautifulSoup(html, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
        return text if text.strip() else None
    except Exception:
        return None
