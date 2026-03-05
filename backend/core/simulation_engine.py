from typing import Dict, Any

from backend.core.world_state import WorldState
from backend.models.agent_decision import AgentDecision


class SimulationEngine:
    """
    Processes agent decisions and updates the world state.
    """
    def __init__(self, world_state: WorldState):
        self.world_state = world_state

    def process_decision(self, agent_name: str, decision: AgentDecision):
        """
        Processes an agent's decision, updating the world state and logging the event.
        """
        if decision.impact:
            self.world_state.update_state(decision.impact)

        event = {
            "day": self.world_state.get_state()['current_day'],
            "agent": agent_name,
            "analysis": decision.analysis,
            "recommendation": decision.recommendation,
            "impact": decision.impact
        }
        self.world_state.add_event(event)

    def get_world_status(self) -> Dict[str, Any]:
        """
        Returns the current status of the world.
        """
        state = self.world_state.get_state()
        # This is a placeholder for active agents, as we don't have a way to track them yet
        state['active_agents'] = 5 
        return state
