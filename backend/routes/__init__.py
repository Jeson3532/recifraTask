from fastapi import APIRouter

from .support import router as ml_router

all_routers = [v for v in list(globals().values()) if isinstance(v, APIRouter)]
