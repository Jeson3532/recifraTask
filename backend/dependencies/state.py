from fastapi import Request
from backend.services.ml.engine import ModelService


def get_model(request: Request) -> ModelService:
    return request.app.state.model
