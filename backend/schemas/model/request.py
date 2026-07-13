from pydantic import BaseModel, Field

class ModelRequest(BaseModel):
    text: str = Field(..., min_length=3, max_length=2048)
