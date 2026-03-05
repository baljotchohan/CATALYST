from abc import ABC, abstractmethod
from backend.core.simulation_engine import SimulationEngine
from backend.models.agent_decision import AgentDecision

class Agent(ABC):
    def __init__(self, name: str, simulation_engine: SimulationEngine):
        self.name = name
        self.simulation_engine = simulation_engine

    @abstractmethod
    def run(self) -> AgentDecision:
        pass

    def apply_impact(self, decision: AgentDecision):
        self.simulation_engine.process_decision(self.name, decision)
