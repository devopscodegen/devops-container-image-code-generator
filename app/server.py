"""
This module exposes the chain using langserve fastapi server
"""

import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from langserve import add_routes
from app.chain import (
    chain as devops_container_image_code_generator_chain,
)


loglevel = os.getenv("DEVOPS_CONTAINER_IMAGE_CODE_GENERATOR_LOG_LEVEL", "WARNING")
numeric_level = getattr(logging, loglevel.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError(f"Invalid log level: {loglevel}")
logging.getLogger().setLevel(level=numeric_level)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/")
async def redirect_root_to_docs():
    """
    This function redirects context path / to api docs /docs
    """
    return RedirectResponse("/docs")


add_routes(
    app,
    devops_container_image_code_generator_chain,
    path="/devops-container-image-code-generator",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
