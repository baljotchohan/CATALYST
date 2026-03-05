from backend.core.simulation_engine import SimulationEngine
from backend.agents.unified_agent import WeatherAgent

async def run_weather_agent(simulation_engine: SimulationEngine):
    agent = WeatherAgent(simulation_engine)
    await agent.run()
