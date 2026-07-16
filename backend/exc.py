from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


# Auth
class AuthBaseError(Exception):
    ...


class InvalidSecretKey(AuthBaseError):
    ...


class NotFoundSecretKey(AuthBaseError):
    ...


def setup_exceptions(app: FastAPI) -> None:
    @app.exception_handler(InvalidSecretKey)
    async def _(request: Request, exception: InvalidSecretKey):
        return JSONResponse(
            status_code=403,
            content={"detail": "Доступ запрещен, введен неверный ключ"}
        )

    @app.exception_handler(NotFoundSecretKey)
    async def _(request: Request, exception: NotFoundSecretKey):
        return JSONResponse(
            status_code=500,
            content={"detail": "Произошла внутренняя ошибка сервера"}
        )
