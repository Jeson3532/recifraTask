from fastapi import Body, Header
import os
from dotenv import load_dotenv
import secrets
import logging

from backend.exc import InvalidSecretKey, NotFoundSecretKey

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)

SECRET_KEY = os.getenv("SECRET_KEY", None)


def authorize(secret_key=Header(..., description="Ключ доступа")) -> None:
    if SECRET_KEY:
        if not secrets.compare_digest(secret_key, SECRET_KEY):
            raise InvalidSecretKey()
        return
    logger.warning("Секретный ключ не инициализирован")
    raise NotFoundSecretKey("Энд-поинт недоступен")
