"""
Geocoder: resolves location strings to [lat, lng] via Photon API.
"""
import requests

PHOTON_BASE = "https://photon.komoot.io/api/"


def geocode(location: str, country_suffix: str = ", Morocco") -> list[float] | None:
    """
    Query Photon API for location. Appends country_suffix to prioritize local results.
    Returns [latitude, longitude] or None if not found.
    """
    if not location or not location.strip():
        return None
    query = f"{location.strip()}{country_suffix}"
    try:
        r = requests.get(
            PHOTON_BASE,
            params={"q": query, "limit": 1},
            timeout=10,
        )
        r.raise_for_status()
        data = r.json()
        features = data.get("features", [])
        if not features:
            return None
        coords = features[0].get("geometry", {}).get("coordinates")
        if coords and len(coords) >= 2:
            return [float(coords[1]), float(coords[0])]
        return None
    except Exception:
        return None
