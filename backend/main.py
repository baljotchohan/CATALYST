"""
CATALYST - FastAPI Main Application
Universal AI Agent Research Platform API
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
from pydantic import BaseModel, HttpUrl
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.database import SessionLocal, engine, get_db, init_db
from backend.models.agent import Agent, AgentStatus, AgentType
from backend.models.research import AgentDataSource, ResearchLog
from backend.models.user import User
from backend.scheduler import start_scheduler, stop_scheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ─────────────────────────── Lifespan ────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database and start background scheduler on startup."""
    logger.info("CATALYST API starting up...")
    init_db()
    _seed_default_agents()
    start_scheduler()
    yield
    stop_scheduler()
    logger.info("CATALYST API shut down.")


def _seed_default_agents():
    """Seed the 5 default CATALYST agents if they don't exist."""
    db = SessionLocal()
    try:
        if db.query(Agent).count() > 0:
            return

        defaults = [
            {
                "name": "Weather Advisor",
                "type": AgentType.weather,
                "description": (
                    "Analyzes live weather patterns across South Asia and generates "
                    "actionable farming advice for smallholder farmers. Powered by "
                    "Open-Meteo API and Claude AI."
                ),
                "specialization": "Agricultural meteorology for India, Pakistan, Bangladesh",
                "impact_score": 57.4,
            },
            {
                "name": "Health Tracker",
                "type": AgentType.health,
                "description": (
                    "Monitors WHO disease surveillance data and news feeds to detect "
                    "emerging health threats, generates early-warning alerts for authorities."
                ),
                "specialization": "Communicable disease surveillance, South Asia",
                "impact_score": 34.2,
            },
            {
                "name": "Education Analyst",
                "type": AgentType.education,
                "description": (
                    "Identifies schools and regions in South Asia with critical education gaps "
                    "using UNESCO and World Bank data. Recommends targeted interventions."
                ),
                "specialization": "Primary education access, literacy improvement",
                "impact_score": 22.8,
            },
            {
                "name": "Farm Advisor",
                "type": AgentType.farm,
                "description": (
                    "Combines weather forecasts, soil moisture data, and commodity market prices "
                    "to generate precision farming recommendations and optimal market timing."
                ),
                "specialization": "Crop rotation, irrigation scheduling, market timing",
                "impact_score": 89.1,
            },
            {
                "name": "Security Analyst",
                "type": AgentType.security,
                "description": (
                    "Monitors real-time news feeds and public databases to detect security trends, "
                    "generate threat assessments, and alert relevant authorities."
                ),
                "specialization": "Regional threat analysis, crime pattern recognition",
                "impact_score": 15.6,
            },
        ]

        for d in defaults:
            agent = Agent(id=str(uuid4()), status=AgentStatus.idle, created_by="catalyst-system", **d)
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
    github_url: Optional[str] = None
    created_by: Optional[str] = None
    data_sources: Optional[list[str]] = []


class AgentResponse(BaseModel):
    id: str
    name: str
    type: str
    description: str
    specialization: Optional[str]
    github_url: Optional[str]
    created_by: Optional[str]
    status: str
    impact_score: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ResearchLogResponse(BaseModel):
    id: str
    agent_id: str
    result: Optional[str]
    impact_metric: float
    impact_description: Optional[str]
    status: str
    timestamp: datetime

    class Config:
        from_attributes = True


# ─────────────────────────── FastAPI App ─────────────────────────────

app = FastAPI(
    title="CATALYST API",
    description="Universal AI Agent Research Platform — GitHub for AI Research Agents",
    version="1.0.0",
    lifespan=lifespan,
)

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────── Routes: Agents ─────────────────────────────

@app.get("/api/agents", response_model=list[AgentResponse], tags=["Agents"])
def list_agents(
    type: Optional[AgentType] = None,
    search: Optional[str] = None,
    limit: int = Query(default=50, le=100),
    db: Session = Depends(get_db),
):
    """Return all agents, optionally filtered by type or search term."""
    q = db.query(Agent)
    if type:
        q = q.filter(Agent.type == type)
    if search:
        q = q.filter(Agent.name.ilike(f"%{search}%") | Agent.description.ilike(f"%{search}%"))
    return q.order_by(Agent.impact_score.desc()).limit(limit).all()


@app.post("/api/agents", tags=["Agents"])
def create_agent(payload: AgentCreate, db: Session = Depends(get_db)):
    """Create a new agent."""
    agent = Agent(
        id=str(uuid4()),
        name=payload.name,
        type=payload.type,
        description=payload.description,
        specialization=payload.specialization,
        github_url=payload.github_url,
        created_by=payload.created_by,
        status=AgentStatus.idle,
        impact_score=0.0,
    )
    db.add(agent)

    for source_name in (payload.data_sources or []):
        ds = AgentDataSource(
            id=str(uuid4()),
            agent_id=agent.id,
            data_source_type=source_name,
        )
        db.add(ds)

    db.commit()
    db.refresh(agent)
    return {"status": "created", "agent_id": agent.id}


@app.get("/api/agents/{agent_id}", response_model=AgentResponse, tags=["Agents"])
def get_agent(agent_id: str, db: Session = Depends(get_db)):
    """Get full details of a single agent."""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@app.post("/api/agents/{agent_id}/run", tags=["Agents"])
async def trigger_agent(agent_id: str, db: Session = Depends(get_db)):
    """Manually trigger an agent run."""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    if agent.status == AgentStatus.running:
        raise HTTPException(status_code=409, detail="Agent is already running")

    # Import and dispatch the correct agent
    asyncio.create_task(_run_agent_task(agent_id, agent.type, db))
    return {"status": "running", "agent_id": agent_id}


async def _run_agent_task(agent_id: str, agent_type: AgentType, db: Session):
    """Dispatch to the correct agent implementation."""
    from backend.agents.weather_agent import run_weather_agent
    from backend.agents.health_agent import run_health_agent
    from backend.agents.education_agent import run_education_agent
    from backend.agents.farm_agent import run_farm_agent
    from backend.agents.security_agent import run_security_agent

    dispatch = {
        AgentType.weather: run_weather_agent,
        AgentType.health: run_health_agent,
        AgentType.education: run_education_agent,
        AgentType.farm: run_farm_agent,
        AgentType.security: run_security_agent,
    }
    runner = dispatch.get(agent_type)
    if runner:
        try:
            await runner(db, agent_id)
        except Exception as e:
            logger.error(f"Agent {agent_id} run failed: {e}")


# ─────────────────────────── Routes: Research Logs ─────────────────────────────

@app.get("/api/research/{agent_id}", response_model=list[ResearchLogResponse], tags=["Research"])
def get_research_logs(
    agent_id: str,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, le=100),
    db: Session = Depends(get_db),
):
    """Get all research logs for a given agent, paginated."""
    offset = (page - 1) * limit
    logs = (
        db.query(ResearchLog)
        .filter(ResearchLog.agent_id == agent_id)
        .order_by(ResearchLog.timestamp.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return logs


# ─────────────────────────── Routes: Impact ─────────────────────────────

@app.get("/api/impact", tags=["Impact"])
def get_global_impact(db: Session = Depends(get_db)):
    """Return global platform impact metrics."""
    total_agents = db.query(func.count(Agent.id)).scalar() or 0
    total_research = db.query(func.count(ResearchLog.id)).scalar() or 0
    total_impact = db.query(func.sum(ResearchLog.impact_metric)).scalar() or 0.0
    active_agents = db.query(func.count(Agent.id)).filter(Agent.status != AgentStatus.error).scalar() or 0

    return {
        "total_agents": total_agents,
        "active_agents": active_agents,
        "total_research": total_research,
        "total_impact_score": round(float(total_impact), 2),
        "people_helped": int(total_impact),
        "data_sources_connected": 6,
        "countries_monitored": 12,
    }


# ─────────────────────────── Routes: Data Sources ─────────────────────────────

@app.get("/api/data/weather", tags=["Data"])
async def get_weather_data(
    latitude: float = Query(default=31.5, description="Latitude"),
    longitude: float = Query(default=74.3, description="Longitude"),
    city: Optional[str] = None,
):
    """Fetch live weather data from Open-Meteo API."""
    from backend.data_sources.open_meteo import fetch_weather
    try:
        return await fetch_weather(latitude, longitude, city)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Weather API error: {str(e)}")


@app.get("/api/data/health", tags=["Data"])
async def get_health_data():
    """Fetch health indicators from WHO API."""
    from backend.data_sources.who_data import fetch_health_summary
    try:
        return await fetch_health_summary()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"WHO API error: {str(e)}")


@app.get("/api/data/education", tags=["Data"])
async def get_education_data():
    """Fetch education statistics from World Bank / UNESCO."""
    from backend.data_sources.unesco_data import fetch_education_summary
    try:
        return await fetch_education_summary()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Education API error: {str(e)}")


# ─────────────────────────── Health Check ─────────────────────────────

@app.get("/", tags=["Health"])
def root():
    return {
        "name": "CATALYST API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}
