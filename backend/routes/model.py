from fastapi import APIRouter, Depends
from backend.schemas.model.request import ModelRequest
from backend.schemas.model.response import ModelResponse
from backend.dependencies.state import get_model
from backend.services.ml.engine import ModelService
import asyncio

router = APIRouter(prefix="/models", tags=["ML-models", 'ML-модели'])

@router.post("/review-classifier", response_model=ModelResponse)
def get_model_response(
        request: ModelRequest,
        model: ModelService = Depends(get_model),):
    return model.request(request.text)