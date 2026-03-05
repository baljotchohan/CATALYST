from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class AgentDecision:
    analysis: str
    recommendation: str
    impact: Optional[Dict[str, float]] = field(default_factory=dict)
