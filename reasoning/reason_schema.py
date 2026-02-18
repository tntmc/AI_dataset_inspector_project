from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class ReasoningContext:
  dataset_overview: Dict
  missing_summary: Dict
  duplicate_rows: int

@dataclass
class ReasoningResults:
  insights: str
  risk_levels: List[str] = field(default_factory=list)
  recommendations: List[str] = field(default_factory=list)