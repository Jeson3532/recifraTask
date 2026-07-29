from pydantic import BaseModel, Field, field_validator, ConfigDict
from backend.utils.enums import  ResponseCategories, Priorities
import re
from typing import Dict


class ModelRequest(BaseModel):
    text: str = Field(..., min_length=3, max_length=2048)

    @field_validator("text", mode='after')
    @classmethod
    def text_validate(cls, text: str) -> str:
        if ''.join(text.split()).isdigit():
            raise ValueError("Текст не содержит слов")
        emoji_pattern = re.compile(
            '['
            '\U0001F600-\U0001F64F'  # Эмодзи-смайлики
            '\U0001F300-\U0001F5FF'  # Символы и пиктограммы
            '\U0001F680-\U0001F6FF'  # Транспорт и карты
            '\U0001F1E0-\U0001F1FF'  # Флаги
            '\U00002702-\U000027B0'  # Разные символы
            '\U000024C2-\U0001F251'  # Знаки и прочее
            ']+', flags=re.UNICODE
        )
        text_no_emoji = emoji_pattern.sub(r'', text)
        if not text_no_emoji:
            raise ValueError("Текст не содержит слов")
        return text_no_emoji


class SaveRequestModel(BaseModel):
    request_text: str = Field(...)
    category: ResponseCategories = Field(...)
    priority: Priorities = Field(...)
    confidence: float = Field(...)
    probabilities: Dict[str, float] = Field(...)

    model_config = ConfigDict(from_attributes=True)
