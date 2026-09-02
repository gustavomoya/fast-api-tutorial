import logging
import time

from typing import Annotated
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from app.core.logging import configure_logging
from app.core.config import settings
from enum import Enum
from pydantic import BaseModel
from app import models
from app.users.router import router as users_router
from app.auth.router import router as auth_router
from app.projects.router import router as projects_router


configure_logging()

app = FastAPI(
     title=settings.app_name,
     version=settings.app_version,
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(projects_router)

logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    logger.exception(
        "Unhandled exception: %s %s",
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error"
        },
    )
    

@app.middleware("http")
async def log_requests(
    request: Request,
    call_next,
):
    start_time = time.perf_counter()

    response = await call_next(request) 

    duration = time.perf_counter() - start_time

    logger.info(
        "%s %s -> %s (%.3fs)",
        request.method,
        request.url.path,
        response.status_code,
        duration,
    )

    return response

