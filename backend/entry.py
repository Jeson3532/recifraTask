from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
import logging

from backend.routes import all_routers
from backend.services.ml.engine import load_model
from backend.exc import setup_exceptions
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = load_model()
    logger.info("Backend Up")
    yield
    logger.info("Backend Down")


app = FastAPI(
    title='API Recifra',
    description='Интерфейс для доступа к ML-модели',
    lifespan=lifespan)

# init routers
for router in all_routers:
    app.include_router(router)

# init exceptions
setup_exceptions(app=app)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
