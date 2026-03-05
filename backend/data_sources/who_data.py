"""
CATALYST - WHO Health Data Source
Fetches disease surveillance and health indicator data from WHO APIs.
"""
import httpx
from typing import Optional


WHO_BASE = "https://ghoapi.azureedge.net/api"


async def fetch_disease_indicators(indicator_code: str = "MALARIA_ESTIMATED_CASES") -> dict:
    """
    Fetch disease data from WHO Global Health Observatory API.

    Args:
        indicator_code: WHO indicator code

    Returns:
        dict with health indicator data
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{WHO_BASE}/{indicator_code}",
            params={"$top": 100, "$orderby": "TimeDim desc"},
        )
        response.raise_for_status()
        return response.json()


async def fetch_mortality_data() -> dict:
    """Fetch mortality rate data."""
    return await fetch_disease_indicators("WHOSIS_000001")


async def fetch_vaccination_coverage() -> dict:
    """Fetch vaccination coverage data."""
    return await fetch_disease_indicators("WHS4_544")


async def fetch_health_summary() -> dict:
    """
    Compile a health data summary from multiple WHO indicators.
    Returns aggregated health metrics.
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Fetch multiple indicators concurrently
            import asyncio
            results = await asyncio.gather(
                client.get(f"{WHO_BASE}/WHOSIS_000001", params={"$top": 20, "$orderby": "TimeDim desc"}),
                client.get(f"{WHO_BASE}/WHS4_544", params={"$top": 20, "$orderby": "TimeDim desc"}),
                return_exceptions=True
            )

        data = {}
        indicators = ["mortality_rate", "vaccination_coverage"]
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                data[indicators[i]] = {"error": str(result)}
            else:
                data[indicators[i]] = result.json()

        return data
    except Exception as e:
        return {"error": str(e), "source": "WHO API"}


# Disease alert threshold - flag any indicator above this z-score
ALERT_THRESHOLD = 2.0
