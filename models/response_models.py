"""Response and evaluation models."""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class FinalAnswer(BaseModel):
    """Represents the agent's final answer."""
    answer: str = Field(description="The agent's answer to the question")
    source_ids: List[str] = Field(description="List of email message IDs used as sources")
    confidence: Optional[float] = Field(default=None, description="Confidence score (0-1)")

class CorrectnessJudgeResponse(BaseModel):
    """Response from the correctness evaluation judge."""
    reasoning: str = Field(description="Explanation of the reasoning process")
    accept: bool = Field(description="Whether the AI answer should be accepted")
    score: Optional[float] = Field(default=None, description="Numerical score (0-1)")

class AgentTrajectory(BaseModel):
    """Represents an agent's execution trajectory."""
    scenario_id: str
    final_answer: Optional[FinalAnswer] = None
    metrics: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def add_metric(self, key: str, value: Any) -> None:
        """Add a metric to the trajectory."""
        self.metrics[key] = value
    
    def is_correct(self) -> Optional[bool]:
        """Check if the trajectory was marked as correct."""
        return self.metrics.get("correct")

class AgentExecutionResult(BaseModel):
    """Result of agent execution."""
    success: bool
    trajectory: Optional[AgentTrajectory] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None