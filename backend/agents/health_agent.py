from backend.core.simulation_engine import SimulationEngine
from backend.agents.unified_agent import HealthAgent

async def run_health_agent(simulation_engine: SimulationEngine):
    agent = HealthAgent(simulation_engine)
    await agent.run()
