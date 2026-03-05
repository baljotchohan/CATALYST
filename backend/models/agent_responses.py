from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime

# UNIFIED RESPONSE MODEL (All agents use this)
class AgentResponse(BaseModel):
    agent_name: str
    agent_type: str
    timestamp: str
    status: str  # "success" or "partial" (if using fallback data)
    
    # Core metrics
    people_reached: int
    impact_metric: float
    confidence_score: float
    
    # Data
    primary_data: Dict
    analysis: str
    recommendations: List[str]
    
    # Sources
    data_sources_used: List[str]
    last_updated: str

class WeatherAgentResponse(AgentResponse):
    agent_type: str = "weather"
    agent_name: str = "Weather Advisor"
    
    primary_data: Dict = {
        "regions": Dict,
        "temperature": float,
        "rainfall_probability": float,
        "soil_moisture": float,
        "wind_speed": float,
        "forecast_7_day": List[Dict]
    }

class HealthAgentResponse(AgentResponse):
    agent_type: str = "health"
    agent_name: str = "Health Tracker"
    
    primary_data: Dict = {
        "disease_trends": Dict,
        "outbreak_alerts": List[Dict],
        "infection_rate": float,
        "affected_regions": List[str],
        "mortality_rate": float
    }

class EducationAgentResponse(AgentResponse):
    agent_type: str = "education"
    agent_name: str = "Education Analyst"
    
    primary_data: Dict = {
        "schools_analyzed": int,
        "performance_metrics": Dict,
        "student_enrollment": Dict,
        "resource_gaps": List[str],
        "recommended_interventions": List[Dict]
    }

class FarmAgentResponse(AgentResponse):
    agent_type: str = "farm"
    agent_name: str = "Farm Advisor"
    
    primary_data: Dict = {
        "commodity_prices": Dict,
        "weather_summary": Dict,
        "soil_conditions": Dict,
        "crop_recommendations": List[Dict],
        "irrigation_schedule": Dict,
        "market_timing": Dict
    }

class SecurityAgentResponse(AgentResponse):
    agent_type: str = "security"
    agent_name: str = "Security Analyst"
    
    primary_data: Dict = {
        "crime_trends": Dict,
        "alerts": List[Dict],
        "hotspots": List[Dict],
        "incident_analysis": Dict,
        "prevention_recommendations": List[str]
    }
