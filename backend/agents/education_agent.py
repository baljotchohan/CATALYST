from backend.core.simulation_engine import SimulationEngine
from backend.agents.unified_agent import EducationAgent

async def run_education_agent(simulation_engine: SimulationEngine):
    agent = EducationAgent(simulation_engine)
    await agent.run()
