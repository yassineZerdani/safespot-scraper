"""
AI extractor: uses Gemini 2.5 Flash to extract incident data from raw text.
"""
import json
import os
from google import genai
from google.genai import types

SYSTEM_INSTRUCTION = """You extract safety incident data from news text.
Return STRICTLY valid JSON with no markdown, no code blocks, no extra text.
Format: {"location": "place name or address", "incident_type": "e.g. theft, accident, fire", "severity_score": 0-100}
If the text is NOT about an incident, danger, crime, accident, or fire, return exactly: null
severity_score: 0-100, higher = more severe. Use 80 for serious incidents."""


def extract_incident(raw_text: str) -> dict | None:
    """
    Pass raw text to Gemini 2.5 Flash. Returns parsed incident dict or None.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=raw_text[:15000],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            response_mime_type="application/json",
        ),
    )
    text = response.text.strip()
    if not text or text.lower() == "null":
        return None
    try:
        data = json.loads(text)
        if isinstance(data, dict) and data.get("location") and data.get("incident_type"):
            return data
        return None
    except json.JSONDecodeError:
        return None
