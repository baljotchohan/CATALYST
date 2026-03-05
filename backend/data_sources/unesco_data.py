"""
CATALYST - UNESCO Education Data Source
Fetches education statistics from UNESCO Institute for Statistics API.
"""
import httpx


UNESCO_BASE = "http://api.uis.unesco.org/sdmx/v2"
# UIS SDMX API (free, no key required for public datasets)
UIS_BASE = "https://api.uis.unesco.org/api/public/sdmx/rest"


async def fetch_literacy_rates(area_code: str = "PAK") -> dict:
    """
    Fetch literacy rate data for a country.

    Args:
        area_code: ISO 3-letter country code

    Returns:
        dict with literacy rate data
    """
    # Use World Bank API as backup for education data (free, no key)
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"https://api.worldbank.org/v2/country/{area_code}/indicator/SE.ADT.LITR.ZS",
            params={"format": "json", "mrv": 5, "per_page": 10},
        )
        response.raise_for_status()
        return response.json()


async def fetch_school_enrollment(area_code: str = "PAK") -> dict:
    """Fetch primary school enrollment ratio."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"https://api.worldbank.org/v2/country/{area_code}/indicator/SE.PRM.ENRR",
            params={"format": "json", "mrv": 5, "per_page": 10},
        )
        response.raise_for_status()
        return response.json()


async def fetch_education_summary(countries: list[str] = None) -> dict:
    """
    Fetch education stats for multiple countries.

    Args:
        countries: List of ISO 3-letter country codes

    Returns:
        dict with education indicators per country
    """
    if countries is None:
        countries = ["IND", "PAK", "BGD", "NPL", "LKA"]

    import asyncio
    results = {}

    async with httpx.AsyncClient(timeout=30.0) as client:
        for country in countries:
            try:
                literacy_resp = await client.get(
                    f"https://api.worldbank.org/v2/country/{country}/indicator/SE.ADT.LITR.ZS",
                    params={"format": "json", "mrv": 3, "per_page": 5},
                )
                enrollment_resp = await client.get(
                    f"https://api.worldbank.org/v2/country/{country}/indicator/SE.PRM.ENRR",
                    params={"format": "json", "mrv": 3, "per_page": 5},
                )
                results[country] = {
                    "literacy": literacy_resp.json(),
                    "enrollment": enrollment_resp.json(),
                }
            except Exception as e:
                results[country] = {"error": str(e)}

    return results
