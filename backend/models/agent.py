"""
CATALYST - Agent SQLAlchemy Model
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from backend.database import Base
import enum


class AgentType(str, enum.Enum):
    weather = "weather"
    health = "health"
    education = "education"
    farm = "farm"
    security = "security"


class AgentStatus(str, enum.Enum):
    active = "active"
    idle = "idle"
    running = "running"
    error = "error"


class Agent(Base):
    """Represents a research agent uploaded to Catalyst."""

    __tablename__ = "agents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False, index=True)
    type = Column(Enum(AgentType), nullable=False, index=True)
    description = Column(Text, nullable=False)
    specialization = Column(Text, nullable=True)
    github_url = Column(String(500), nullable=True)
    created_by = Column(String(255), nullable=True)
    status = Column(Enum(AgentStatus), default=AgentStatus.idle)
    impact_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    research_logs = relationship("ResearchLog", back_populates="agent", cascade="all, delete-orphan")
    data_sources = relationship("AgentDataSource", back_populates="agent", cascade="all, delete-orphan")
