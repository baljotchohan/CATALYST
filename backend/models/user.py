"""
CATALYST - User SQLAlchemy Model
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text
from backend.database import Base


class User(Base):
    """Platform users who upload and manage agents."""

    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    github_username = Column(String(255), nullable=True, unique=True)
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
