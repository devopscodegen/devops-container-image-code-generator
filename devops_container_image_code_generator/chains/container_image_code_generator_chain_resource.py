"""
PLACEHOLDER
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from langserve import add_routes
from .container_image_code_generator_chain_application_service import (
    ContainerImageCodeGeneratorChainApplicationService,
)


class ContainerImageCodeGeneratorChainResource:
    """
    PLACEHOLDER
    """

    def __init__(self, app: FastAPI = None):
        self.set_app(app)

    def get_app(self) -> FastAPI:
        """Get app"""
        return self.app

    def set_app(self, app: FastAPI = None):
        """Set llm"""
        self.app = app

    def create_fastapi_app(self) -> FastAPI:
        """PLACEHOLDER"""

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
            ContainerImageCodeGeneratorChainApplicationService().create_chain(),
            path="/devops-container-image-code-generator",
        )

        self.set_app(app)
        return app
