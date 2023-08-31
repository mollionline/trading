import logging
from fastapi import APIRouter, FastAPI
from .config import settings
from .http_client import http_client  # do not change place of this import
from project.trades import views

"""Create app factory"""


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        debug=True,
    )

    @app.on_event("startup")
    async def startup_event():
        logger = logging.getLogger("uvicorn.access")
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(handler)
        file_handler_info = logging.FileHandler("uvicorn_info_log.log", mode="a")
        file_handler_info.setLevel(logging.INFO)
        logger.addHandler(file_handler_info)
        logger_error = logging.getLogger("uvicorn.error")
        file_handler_error = logging.FileHandler("uvicorn_error_log.log", mode="a")
        file_handler_error.setLevel(logging.ERROR)
        logger_error.addHandler(file_handler_error)

    routes = APIRouter()

    @routes.on_event("startup")
    async def startup():
        http_client.start()

    @routes.on_event("shutdown")
    async def shutdown():
        await http_client.stop()

    routes.include_router(views.trade_router, prefix=settings.WWW_DOMAIN)
    app.include_router(routes)
    return app
