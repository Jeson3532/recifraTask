from pydantic import BaseModel, Field
from typing import Dict

class ModelResponse(BaseModel):
    category: str = Field(...)
    priority: str = Field(...)
    confidence: float = Field(...)
    probabilities: Dict[str, float] = Field(...)
