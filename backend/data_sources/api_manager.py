import httpx
import asyncio
from datetime import datetime, timedelta
import json

class APIManager:
    """Unified API manager with fallback data"""
    
    FALLBACK_DATA = {
        "weather": {
            "regions": {
                "punjab": {"temp": 28, "humidity": 65, "rainfall_prob": 45},
                "sindh": {"temp": 32, "humidity": 55, "rainfall_prob": 30},
                "haryana": {"temp": 26, "humidity": 70, "rainfall_prob": 50}
            },
            "temperature": 28.5,
            "rainfall_probability": 45,
            "soil_moisture": 52,
            "wind_speed": 12,
            "forecast_7_day": [
                {"day": "Monday", "temp_max": 32, "temp_min": 18, "rainfall": 40},
                {"day": "Tuesday", "temp_max": 30, "temp_min": 17, "rainfall": 35},
                {"day": "Wednesday", "temp_max": 28, "temp_min": 16, "rainfall": 60}
            ]
        },
        "prices": {
            "wheat": {"price": 2650, "trend": "up", "unit": "INR/quintal"},
            "rice": {"price": 3400, "trend": "stable", "unit": "INR/quintal"},
            "corn": {"price": 2100, "trend": "down", "unit": "INR/quintal"},
            "cotton": {"price": 6850, "trend": "up", "unit": "INR/kg"}
        },
        "health": {
            "disease_trends": {
                "respiratory": {"cases": 1250000, "trend": "up", "growth_rate": 5.2},
                "dengue": {"cases": 450000, "trend": "down", "growth_rate": -2.1},
                "malaria": {"cases": 320000, "trend": "stable", "growth_rate": 0.3}
            },
            "outbreak_alerts": [
                {"disease": "Respiratory", "regions": ["Punjab", "Delhi"], "severity": "moderate"},
                {"disease": "Dengue", "regions": ["Maharashtra"], "severity": "low"}
            ]
        },
        "crime": {
            "crime_trends": {
                "theft": {"incidents": 15000, "trend": "down", "month_over_month": -3.2},
                "assault": {"incidents": 8500, "trend": "up", "month_over_month": 2.1},
                "cyber": {"incidents": 5200, "trend": "up", "month_over_month": 8.5}
            },
            "hotspots": [
                {"city": "Delhi", "crime_type": "theft", "incidents": 3200},
                {"city": "Mumbai", "crime_type": "assault", "incidents": 2100}
            ]
        },
        "education": {
            "schools_analyzed": 15000,
            "performance_metrics": {
                "avg_literacy_rate": 78.5,
                "avg_enrollment": 450,
                "dropout_rate": 12.3
            },
            "resource_gaps": [
                "Missing trained teachers",
                "Lack of digital infrastructure",
                "Inadequate sanitation"
            ]
        }
    }
    
    @staticmethod
    async def fetch_weather(latitude=31.5, longitude=74.3, timeout=5):
        """Fetch from Open-Meteo with fallback"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.open-meteo.com/v1/forecast",
                    params={
                        "latitude": latitude,
                        "longitude": longitude,
                        "hourly": "temperature_2m,precipitation_probability,soil_moisture,wind_speed_10m",
                        "daily": "temperature_2m_max,temperature_2m_min,precipitation,precipitation_probability",
                        "timezone": "Asia/Kolkata"
                    },
                    timeout=timeout
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "temperature": data["hourly"]["temperature_2m"][0],
                        "rainfall_probability": data["hourly"]["precipitation_probability"][0],
                        "soil_moisture": data["hourly"]["soil_moisture"][0],
                        "wind_speed": data["hourly"]["wind_speed_10m"][0],
                        "forecast_7_day": data["daily"],
                        "status": "live"
                    }
        except Exception as e:
            print(f"Weather API error: {e}")
        
        return {**APIManager.FALLBACK_DATA["weather"], "status": "fallback"}
    
    @staticmethod
    async def fetch_commodity_prices(timeout=5):
        """Fetch prices with multiple fallbacks"""
        try:
            async with httpx.AsyncClient() as client:
                # Try APIFarmer first
                response = await client.get(
                    "https://api.apinarmer.com/v1/commodities",
                    params={"region": "india"},
                    timeout=timeout
                )
                
                if response.status_code == 200:
                    return {"data": response.json(), "status": "live"}
        except:
            pass
        
        # Try fallback source
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://agmarknet.gov.in/",
                    timeout=timeout
                )
                if response.status_code == 200:
                    return {"data": response.json(), "status": "live"}
        except:
            pass
        
        # Return fallback data
        return {"data": APIManager.FALLBACK_DATA["prices"], "status": "fallback"}
    
    @staticmethod
    async def fetch_health_data(timeout=5):
        """Fetch health data with fallback"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://covid19.who.int/data",
                    timeout=timeout
                )
                if response.status_code == 200:
                    return {"data": response.json(), "status": "live"}
        except:
            pass
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://pubmed.ncbi.nlm.nih.gov/api/",
                    timeout=timeout
                )
                if response.status_code == 200:
                    return {"data": response.json(), "status": "live"}
        except:
            pass
        
        return {"data": APIManager.FALLBACK_DATA["health"], "status": "fallback"}
    
    @staticmethod
    async def fetch_crime_data(timeout=5):
        """Fetch crime data with fallback"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://data.worldbank.org/indicator/",
                    timeout=timeout
                )
                if response.status_code == 200:
                    return {"data": response.json(), "status": "live"}
        except:
            pass
        
        return {"data": APIManager.FALLBACK_DATA["crime"], "status": "fallback"}
    
    @staticmethod
    async def fetch_education_data(timeout=5):
        """Fetch education data with fallback"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://data.unicef.org/wp-json/",
                    timeout=timeout
                )
                if response.status_code == 200:
                    return {"data": response.json(), "status": "live"}
        except:
            pass
        
        return {"data": APIManager.FALLBACK_DATA["education"], "status": "fallback"}
