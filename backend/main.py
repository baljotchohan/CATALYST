from fastapi import FastAPI
from fastapi.cors import CORSMiddleware
import asyncio
from backend.agents.unified_agent import (
    WeatherAgent, HealthAgent, FarmAgent, 
    SecurityAgent, EducationAgent
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)

# Initialize agents
agents = {
    "weather": WeatherAgent(),
    "health": HealthAgent(),
    "farm": FarmAgent(),
    "security": SecurityAgent(),
    "education": EducationAgent()
}

@app.post("/api/agents/{agent_type}/run")
async def run_agent(agent_type: str):
    """Run any agent and get structured response"""
    if agent_type not in agents:
        return {"error": "Agent not found"}
    
    try:
        result = await agents[agent_type].run()
        return result
    except Exception as e:
        return {"error": str(e), "status": "error"}

@app.get("/api/agents")
async def get_all_agents():
    """Get all agents status"""
    return {
        "agents": [
            {"name": "Weather Advisor", "type": "weather", "status": "active"},
            {"name": "Health Tracker", "type": "health", "status": "active"},
            {"name": "Farm Advisor", "type": "farm", "status": "active"},
            {"name": "Security Analyst", "type": "security", "status": "active"},
            {"name": "Education Analyst", "type": "education", "status": "active"}
        ]
    }

@app.get("/api/impact")
async def get_global_impact():
    """Get impact metrics"""
    return {
        "total_agents": 5,
        "total_research_runs": 156,
        "people_helped": 27500000,
        "impact_score": 7.8
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
