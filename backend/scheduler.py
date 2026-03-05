"""
CIVION - Background Scheduler
Runs the 5 research agents on their defined schedules using APScheduler.
"""
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from backend.core.world_state import WorldState
from backend.core.simulation_engine import SimulationEngine
from backend.agents.weather_agent import run_weather_agent
from backend.agents.health_agent import run_health_agent
from backend.agents.education_agent import run_education_agent
from backend.agents.farm_agent import run_farm_agent
from backend.agents.security_agent import run_security_agent

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()

# Initialize WorldState and SimulationEngine
world_state = WorldState()
simulation_engine = SimulationEngine(world_state)

def start_scheduler():
    """Configure and start all agent job schedules."""

    async def run_agent(runner):
        try:
            await runner(simulation_engine)
        except Exception as e:
            logger.error(f"Scheduled run failed for {runner.__name__}: {e}")

    # Schedule for all agents
    scheduler.add_job(
        lambda: run_agent(run_weather_agent),
        IntervalTrigger(minutes=1),  # For demonstration purposes, runs every minute
        id="weather_agent",
        name="Weather Advisor",
        replace_existing=True,
    )

    scheduler.add_job(
        lambda: run_agent(run_health_agent),
        IntervalTrigger(minutes=1, start_date="2024-01-01T00:01:00Z"),
        id="health_agent",
        name="Health Tracker",
        replace_existing=True,
    )

    scheduler.add_job(
        lambda: run_agent(run_education_agent),
        IntervalTrigger(minutes=1, start_date="2024-01-01T00:02:00Z"),
        id="education_agent",
        name="Education Analyst",
        replace_existing=True,
    )

    scheduler.add_job(
        lambda: run_agent(run_farm_agent),
        IntervalTrigger(minutes=1, start_date="2024-01-01T00:03:00Z"),
        id="farm_agent",
        name="Farm Advisor",
        replace_existing=True,
    )

    scheduler.add_job(
        lambda: run_agent(run_security_agent),
        IntervalTrigger(minutes=1, start_date="2024-01-01T00:04:00Z"),
        id="security_agent",
        name="Security Analyst",
        replace_existing=True,
    )
    
    # A job to increment the day
    scheduler.add_job(
        world_state.increment_day,
        IntervalTrigger(days=1),
        id="increment_day",
        name="Increment Day",
        replace_existing=True,
    )

    scheduler.start()
    logger.info(f"Scheduler started with {len(scheduler.get_jobs())} jobs.")


def stop_scheduler():
    """Gracefully stop the scheduler."""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Scheduler stopped")
