"""
CATALYST - News & Security Data Source
Uses NewsAPI (free tier) + fallback to RSS feeds for event tracking.
"""
import os
import httpx
from typing import Optional


NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
NEWSAPI_BASE = "https://newsapi.org/v2"

# Fallback: GDELT Project (completely free, no key)
GDELT_BASE = "https://api.gdeltproject.org/api/v2/doc/doc"


async def fetch_security_news(
    query: str = "crime security threat alert",
    country: str = "in",
    page_size: int = 20,
) -> dict:
    """
    Fetch recent security/crime-related news.

    Args:
        query: Search query string
        country: 2-letter country code
        page_size: Number of articles

    Returns:
        dict with news articles
    """
    if NEWS_API_KEY:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{NEWSAPI_BASE}/everything",
                params={
                    "q": query,
                    "sortBy": "publishedAt",
                    "pageSize": page_size,
                    "apiKey": NEWS_API_KEY,
                    "language": "en",
                },
            )
            if response.status_code == 200:
                return response.json()

    # Fallback: GDELT free API
    return await fetch_gdelt_events(query)


async def fetch_gdelt_events(
    query: str = "security crime",
    mode: str = "artlist",
    max_records: int = 10,
) -> dict:
    """
    Fetch events from GDELT Project (completely free, no API key needed).
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            GDELT_BASE,
            params={
                "query": query,
                "mode": mode,
                "maxrecords": max_records,
                "format": "json",
                "timespan": "24h",
            },
        )
        if response.status_code == 200:
            return response.json()
        return {"articles": [], "source": "GDELT", "totalResults": 0}


async def fetch_health_alerts(region: str = "South Asia") -> dict:
    """Fetch health emergency alerts from news."""
    return await fetch_security_news(
        query=f"disease outbreak epidemic health emergency {region}",
        page_size=15,
    )


async def fetch_weather_alerts(region: str = "South Asia") -> dict:
    """Fetch extreme weather events from news."""
    return await fetch_security_news(
        query=f"flood drought cyclone heat wave {region} farmer",
        page_size=15,
    )
