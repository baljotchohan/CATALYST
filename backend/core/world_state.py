import json
import os
from typing import Dict, Any, List

class WorldState:
    """
    Manages the state of the simulated world.
    """
    def __init__(self, state_file: str = 'world_state.json'):
        self.state_file = state_file
        self._state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        """Loads state from file, or returns initial state."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass  # Fallback to initial state if file is corrupt or unreadable
        return {
            "current_day": 1,
            "gdp": 5000,
            "stability": 70,
            "resources": 80,
            "dominant_ideology": "Technocratic",
            "global_impact_score": 0,
            "recent_events": []
        }

    def _save_state(self):
        """Saves the current state to the file."""
        with open(self.state_file, 'w') as f:
            json.dump(self._state, f, indent=4)

    def get_state(self) -> Dict[str, Any]:
        """Returns a copy of the current state."""
        return self._state.copy()

    def update_state(self, updates: Dict[str, float]):
        """
        Updates the world state with the given values.
        Only updates numerical values by adding to them.
        """
        for key, value in updates.items():
            if key in self._state and isinstance(self._state[key], (int, float)):
                self._state[key] += value
        self._save_state()

    def add_event(self, event: Dict[str, Any]):
        """Adds a new event to the recent events list."""
        self._state['recent_events'].insert(0, event)
        # Keep the list of recent events from growing too large
        if len(self._state['recent_events']) > 100:
            self._state['recent_events'].pop()
        self._save_state()

    def increment_day(self):
        """Increments the current day."""
        self._state['current_day'] += 1
        self._save_state()
