"""
CATALYST - Open-Meteo Weather Data Source
Fetches free weather data - no API key required.
"""
import httpx
from typing import Optional


OPEN_METEO_BASE = "https://api.open-meteo.com/v1"


async def fetch_weather(
    latitude: float,
    longitude: float,
    city: Optional[str] = None
) -> dict:
    """
    Fetch current and forecast weather data for a location.

    Args:
        latitude: Location latitude
        longitude: Location longitude
        city: Optional city name for display

    Returns:
        dict with weather data including temperature, wind, precipitation
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "wind_speed_10m",
            "wind_direction_10m",
            "precipitation",
            "weather_code",
            "cloud_cover",
        ],
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "wind_speed_10m_max",
            "et0_fao_evapotranspiration",
            "soil_moisture_0_to_1cm",
        ],
        "forecast_days": 7,
        "timezone": "auto",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f"{OPEN_METEO_BASE}/forecast", params=params)
        response.raise_for_status()
        data = response.json()

    return {
        "city": city,
        "latitude": latitude,
        "longitude": longitude,
        "timezone": data.get("timezone"),
        "current": data.get("current", {}),
        "daily": data.get("daily", {}),
        "units": data.get("current_units", {}),
    }


# Key farming regions (South Asia focus)
FARMING_REGIONS = [
    {"name": "Punjab, Pakistan", "lat": 31.5497, "lon": 74.3436},
    {"name": "Punjab, India", "lat": 30.9010, "lon": 75.8573},
    {"name": "Dhaka, Bangladesh", "lat": 23.8103, "lon": 90.4125},
    {"name": "Maharashtra, India", "lat": 19.7515, "lon": 75.7139},
    {"name": "Sindh, Pakistan", "lat": 25.8943, "lon": 68.5247},
]


async def fetch_farming_regions_weather() -> list[dict]:
    """Fetch weather for all key farming regions."""
    results = []
    for region in FARMING_REGIONS:
        try:
            data = await fetch_weather(region["lat"], region["lon"], region["name"])
            results.append(data)
        except Exception as e:
            results.append({"city": region["name"], "error": str(e)})
    return results
