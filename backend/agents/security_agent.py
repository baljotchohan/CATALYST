from backend.core.simulation_engine import SimulationEngine
from backend.agents.unified_agent import SecurityAgent

async def run_security_agent(simulation_engine: SimulationEngine):
    agent = SecurityAgent(simulation_engine)
    await agent.run()
