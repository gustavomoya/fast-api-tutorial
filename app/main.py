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
from app.tasks.router import router as tasks_router
# import httpx


configure_logging()

app = FastAPI(
     title=settings.app_name,
     version=settings.app_version,
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(projects_router)
app.include_router(tasks_router)

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

# @app.get("/external")
# async def root():
#     # url = "http://127.0.0.1:3001/api/blogs"
#     url = "https://jsonplaceholder.typicode.com/posts"

#     try:
#         async with httpx.AsyncClient() as client:
#             response = await client.get(url)

#         # response.raise_for_status()

#         return response.json()

#     except httpx.HTTPStatusError as e:
#         raise HTTPException(
#             status_code=e.response.status_code,
#             detail="La API de blogs respondió con un error"
#         )

#     except httpx.RequestError as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"No se pudo conectar con la API de blogs: {str(e)}"
#         )
