"""
CATALYST - Background Scheduler
Runs the 5 research agents on their defined schedules using APScheduler.
"""
import logging
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


def start_scheduler():
    """Configure and start all agent job schedules."""
    from backend.database import SessionLocal
    from backend.agents.weather_agent import run_weather_agent
    from backend.agents.health_agent import run_health_agent
    from backend.agents.education_agent import run_education_agent
    from backend.agents.farm_agent import run_farm_agent
    from backend.agents.security_agent import run_security_agent
    from backend.models.agent import Agent, AgentType

    def get_agent_id(agent_type: AgentType) -> str:
        db = SessionLocal()
        try:
            agent = db.query(Agent).filter(Agent.type == agent_type).first()
            return agent.id if agent else None
        finally:
            db.close()

    async def run_with_session(runner, agent_type):
        db = SessionLocal()
        try:
            agent_id = get_agent_id(agent_type)
            if agent_id:
                await runner(db, agent_id)
        except Exception as e:
            logger.error(f"Scheduled run failed for {agent_type}: {e}")
        finally:
            db.close()

    # Weather: every 6 hours
    scheduler.add_job(
        lambda: __import__("asyncio").create_task(run_with_session(run_weather_agent, AgentType.weather)),
        IntervalTrigger(hours=6),
        id="weather_agent",
        name="Weather Advisor",
        replace_existing=True,
    )

    # Health: every 24 hours
    scheduler.add_job(
        lambda: __import__("asyncio").create_task(run_with_session(run_health_agent, AgentType.health)),
        IntervalTrigger(hours=24),
        id="health_agent",
        name="Health Tracker",
        replace_existing=True,
    )

    # Education: every week (Monday 06:00 UTC)
    scheduler.add_job(
        lambda: __import__("asyncio").create_task(run_with_session(run_education_agent, AgentType.education)),
        CronTrigger(day_of_week="mon", hour=6),
        id="education_agent",
        name="Education Analyst",
        replace_existing=True,
    )

    # Farm: every 6 hours
    scheduler.add_job(
        lambda: __import__("asyncio").create_task(run_with_session(run_farm_agent, AgentType.farm)),
        IntervalTrigger(hours=6),
        id="farm_agent",
        name="Farm Advisor",
        replace_existing=True,
    )

    # Security: every 4 hours
    scheduler.add_job(
        lambda: __import__("asyncio").create_task(run_with_session(run_security_agent, AgentType.security)),
        IntervalTrigger(hours=4),
        id="security_agent",
        name="Security Analyst",
        replace_existing=True,
    )

    scheduler.start()
    logger.info(f"Scheduler started with {len(scheduler.get_jobs())} agent jobs")


def stop_scheduler():
    """Gracefully stop the scheduler."""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Scheduler stopped")
