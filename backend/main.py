"""
CIVION - FastAPI Main Application
Hybrid AI Civilization Platform API
"""
import asyncio
import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database import SessionLocal, get_db, init_db
from backend.models.agent import Agent, AgentStatus, AgentType
from backend.models.research import ResearchLog
from backend.scheduler import start_scheduler, stop_scheduler, simulation_engine
from backend.core.simulation_engine import SimulationEngine

from backend.agents.unified_agent import (
    WeatherAgent, HealthAgent, FarmAgent, 
    SecurityAgent, EducationAgent
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─────────────────────────── Lifespan ────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database and start background scheduler on startup."""
    logger.info("CIVION API starting up...")
    init_db()
    _seed_default_agents()
    start_scheduler()
    yield
    stop_scheduler()
    logger.info("CIVION API shut down.")

def _seed_default_agents():
    """Seed the 5 default CIVION agents if they don't exist."""
    db = SessionLocal()
    try:
        if db.query(Agent).count() > 0:
            return

        defaults = [
            {"name": "Weather Advisor", "type": AgentType.weather, "description": "Analyzes weather patterns.", "specialization": "Meteorology"},
            {"name": "Health Tracker", "type": AgentType.health, "description": "Monitors health data.", "specialization": "Epidemiology"},
            {"name": "Education Analyst", "type": AgentType.education, "description": "Analyzes education data.", "specialization": "Education Policy"},
            {"name": "Farm Advisor", "type": AgentType.farm, "description": "Provides farming advice.", "specialization": "Agriculture"},
            {"name": "Security Analyst", "type": AgentType.security, "description": "Analyzes security threats.", "specialization": "Security Analysis"},
        ]

        for d in defaults:
            agent = Agent(id=str(uuid4()), status=AgentStatus.idle, created_by="civion-system", **d)
            db.add(agent)
        db.commit()
        logger.info("Seeded 5 default agents.")
    finally:
        db.close()


# ─────────────────────────── Pydantic Schemas ─────────────────────────────

class AgentCreate(BaseModel):
    name: str
    type: AgentType
    description: str
    specialization: Optional[str] = None

class AgentResponse(BaseModel):
    id: str
    name: str
    type: str
    description: str
    specialization: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ResearchLogResponse(BaseModel):
    id: str
    agent_id: str
    result: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True

# ─────────────────────────── FastAPI App ─────────────────────────────

app = FastAPI(
    title="CIVION API",
    description="Hybrid AI Civilization Platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────── Routes: World ─────────────────────────────

@app.get("/api/world/status", tags=["World"])
def get_world_status():
    """Return the current state of the simulated world."""
    return simulation_engine.get_world_status()

# ─────────────────────────── Routes: Agents ─────────────────────────────

@app.get("/api/agents", response_model=list[AgentResponse], tags=["Agents"])
def list_agents(db: Session = Depends(get_db)):
    """Return all agents."""
    return db.query(Agent).all()

@app.post("/api/agents/{agent_id}/run", tags=["Agents"])
async def trigger_agent(agent_id: str, db: Session = Depends(get_db)):
    """Manually trigger an agent run."""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    agent_map = {
        AgentType.weather: WeatherAgent,
        AgentType.health: HealthAgent,
        AgentType.farm: FarmAgent,
        AgentType.security: SecurityAgent,
        AgentType.education: EducationAgent,
    }

    if agent.type not in agent_map:
        raise HTTPException(status_code=400, detail="Agent type not supported for manual execution")

    agent_class = agent_map[agent.type]
    agent_instance = agent_class(simulation_engine)
    
    asyncio.create_task(run_and_log_agent(agent_instance, agent.id, db))
    
    return {"status": "running", "agent_id": agent_id}


async def run_and_log_agent(agent_instance, agent_id, db):
    try:
        decision = await agent_instance.run()
        log = ResearchLog(
            id=str(uuid4()),
            agent_id=agent_id,
            result=f'{{"analysis": "{decision.analysis}", "recommendation": "{decision.recommendation}"}}',
            timestamp=datetime.now()
        )
        db.add(log)
        db.commit()
    except Exception as e:
        logger.error(f"Agent {agent_id} run failed: {e}")

# ─────────────────────────── Health Check ─────────────────────────────

@app.get("/", tags=["Health"])
def root():
    return {
        "name": "CIVION API",
        "version": "1.0.0",
        "status": "operational",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
