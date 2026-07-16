from pydantic import BaseModel, Field
from typing import Dict
from backend.utils.enums import Priorities, ResponseCategories


class ModelResponse(BaseModel):
    category: ResponseCategories = Field(...)
    priority: Priorities = Field(...)
    confidence: float = Field(...)
    probabilities: Dict[str, float] = Field(...)
