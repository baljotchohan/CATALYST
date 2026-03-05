"""
CATALYST - Google APIs Data Source
Civic data sourced from Google Trends and public datasets.
"""
import httpx


# Google Trends via unofficial pytrends-style requests (no API key for basic use)
# Also uses Google's public dataset APIs

async def fetch_commodity_prices() -> dict:
    """
    Fetch commodity prices (wheat, rice, corn) via World Bank Commodity API.
    Completely free, no key required.
    """
    commodities = {
        "wheat": "PWHEAMT",
        "rice": "PRICENPQ",
        "corn": "PMAIZMTUSA",
    }
    results = {}
    async with httpx.AsyncClient(timeout=30.0) as client:
        for name, code in commodities.items():
            try:
                response = await client.get(
                    f"https://api.worldbank.org/v2/en/indicator/{code}",
                    params={"format": "json", "mrv": 12, "per_page": 12},
                )
                results[name] = response.json() if response.status_code == 200 else {"error": "fetch failed"}
            except Exception as e:
                results[name] = {"error": str(e)}
    return results


async def fetch_air_quality(latitude: float, longitude: float) -> dict:
    """
    Fetch air quality data via OpenAQ API (free).
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(
                "https://api.openaq.org/v2/latest",
                params={
                    "coordinates": f"{latitude},{longitude}",
                    "radius": 25000,
                    "limit": 5,
                },
                headers={"X-API-Key": ""},
            )
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass
    return {"results": [], "source": "OpenAQ"}
