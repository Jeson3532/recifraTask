from pydantic import BaseModel, Field

class ModelRequest(BaseModel):
    text: str = Field(...)
