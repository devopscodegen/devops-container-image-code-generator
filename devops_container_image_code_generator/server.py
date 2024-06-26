"""
This module exposes the chain using langserve fastapi server
"""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes
from devops_container_image_code_generator.chain import (
    chain as devops_container_image_code_generator_chain,
)

app = FastAPI()


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
