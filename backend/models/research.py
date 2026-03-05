"""
CATALYST - Research Log SQLAlchemy Model
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.database import Base


class ResearchLog(Base):
    """Stores each research run performed by an agent."""

    __tablename__ = "research_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False, index=True)
    data_input = Column(JSON, nullable=True)
    result = Column(Text, nullable=True)
    insights = Column(JSON, nullable=True)
    impact_metric = Column(Float, default=0.0)
    impact_description = Column(String(500), nullable=True)
    status = Column(String(50), default="completed")
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    agent = relationship("Agent", back_populates="research_logs")


class AgentDataSource(Base):
    """Maps agents to their data sources."""

    __tablename__ = "agent_data_sources"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False, index=True)
    data_source_type = Column(String(100), nullable=False)
    api_endpoint = Column(String(500), nullable=True)
    description = Column(String(255), nullable=True)

    agent = relationship("Agent", back_populates="data_sources")
