from backend.core.simulation_engine import SimulationEngine
from backend.agents.unified_agent import FarmAgent

async def run_farm_agent(simulation_engine: SimulationEngine):
    agent = FarmAgent(simulation_engine)
    await agent.run()
