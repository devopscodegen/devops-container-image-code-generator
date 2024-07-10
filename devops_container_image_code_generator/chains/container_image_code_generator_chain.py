"""
PLACEHOLDER
"""

import importlib
import os
from langchain_core.runnables import RunnableLambda, RunnablePassthrough, Runnable
from devopscodegen_common.repositories import GitSourceCodeRepository
from devopscodegen_common.repositories import SourceCodeRepository
from devopscodegen_common.chains import MiddlewareChain
from .container_image_code_generator_chain_for_middleware import (
    ContainerImageCodeGeneratorChainForMiddleware,
)


class ContainerImageCodeGeneratorChain:
    """
    PLACEHOLDER
    """

    def __init__(
        self,
        llm: Runnable = None,
        source_code_repository: SourceCodeRepository = None,
        chain: Runnable = None,
    ):
        self.set_llm(llm)
        self.set_source_code_repository(source_code_repository)
        self.set_chain(chain)

    def get_llm(self) -> Runnable:
        """Get llm"""
        return self.llm

    def set_llm(self, llm: Runnable = None):
        """Set llm"""
        self.llm = llm

    def get_source_code_repository(self) -> SourceCodeRepository:
        """Get source code repository"""
        return self.source_code_repository

    def set_source_code_repository(
        self, source_code_repository: SourceCodeRepository = None
    ):
        """Set source code repository"""
        self.source_code_repository = source_code_repository

    def get_chain(self) -> Runnable:
        """Get chain"""
        return self.chain

    def set_chain(self, chain: Runnable = None):
        """Set chain"""
        self.chain = chain

    def create_chain(self) -> Runnable:
        """PLACEHOLDER"""
        chain = (
            RunnableLambda(self.runnable_fnd_lang_dep_mfst_dep_mgmt_tool).with_config(
                run_name="fnd_lang_dep_mfst_dep_mgmt_tool"
            )
            | RunnablePassthrough.assign(
                middleware=RunnableLambda(
                    self.route_to_find_middleware_chain
                ).with_config(run_name="route_to_find_middleware_chain")
            ).with_config(run_name="set_middleware")
            | RunnableLambda(
                self.route_to_generate_container_image_code_chain
            ).with_config(run_name="route_to_generate_container_image_code_chain")
        )
        self.set_chain(chain)
        return chain

    def import_module(self, name: str = None, path: str = None):
        """
        This function dynamically imports a Python module from a given file path.
        """
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def runnable_fnd_lang_dep_mfst_dep_mgmt_tool(self, text: str = None):
        """
        Function which takes git source code repository as input and
        returns the language, dependency manifest, dependency manifest content and
        dependency management tool.
        """
        self.set_source_code_repository(
            GitSourceCodeRepository(path=None, url=text, branch="main")
        )
        self.get_source_code_repository().checkout_branch()
        self.get_source_code_repository().fnd_lang_dep_mfst_dep_mgmt_tool()
        language = self.get_source_code_repository().get_language()
        dependency_manifest = (
            self.get_source_code_repository().get_dependency_manifest()
        )
        dependency_manifest_content = (
            self.get_source_code_repository().get_dependency_manifest_content()
        )
        dependency_management_tool = (
            self.get_source_code_repository().get_dependency_management_tool()
        )
        return {
            "language": language,
            "dependency_manifest": dependency_manifest,
            "dependency_manifest_content": dependency_manifest_content,
            "dependency_management_tool": dependency_management_tool,
        }

    def route_to_find_middleware_chain(self, info: dict = None):
        """
        Routing function which returns the find_middleware_chain
        corresponding to the language and dependency management tool
        """
        llm = self.get_llm()
        language = info["language"]
        dependency_management_tool = info["dependency_management_tool"]
        module_name = "find_middleware_chain_module"
        # pylint: disable=R0801
        module_path = os.path.join(
            "app",
            "chains",
            "find_middleware",
            language,
            dependency_management_tool,
            "find_middleware_chain.py",
        )
        if os.path.isfile(module_path):
            find_middleware_chain_module = self.import_module(
                name=module_name, path=module_path
            )
            return find_middleware_chain_module.create_find_middleware_chain(
                llm=llm,
                language=language,
                dependency_management_tool=dependency_management_tool,
            )
        return MiddlewareChain(
            llm=llm,
            source_code_repository=SourceCodeRepository(
                language=language, dependency_management_tool=dependency_management_tool
            ),
        ).create_chain()

    def route_to_generate_container_image_code_chain(self, info: dict = None):
        """
        Routing function which returns the generate_container_image_code_chain
        corresponding to the middleware returned by find_middleware_chain
        """
        llm = self.get_llm()
        language = info["language"]
        dependency_management_tool = info["dependency_management_tool"]
        module_name = "generate_container_image_code_chain_module"
        middleware = info.get("middleware")
        if isinstance(middleware, dict):
            if "middleware" in middleware:
                middleware = middleware["middleware"]
            else:
                raise KeyError(
                    f"middleware key is missing in input middleware dictionary {middleware}"
                )
        # pylint: disable=R0801
        module_path = os.path.join(
            "app",
            "chains",
            "generate_container_image_code",
            language,
            dependency_management_tool,
            middleware,
            "generate_container_image_code_chain.py",
        )
        if os.path.isfile(module_path):
            generate_container_image_code_chain_module = self.import_module(
                name=module_name, path=module_path
            )
            return generate_container_image_code_chain_module.create_generate_container_image_code_chain(
                llm=llm,
                language=language,
                dependency_management_tool=dependency_management_tool,
                middleware=middleware,
            )
        return ContainerImageCodeGeneratorChainForMiddleware(
            llm=llm,
            source_code_repository=SourceCodeRepository(
                language=language,
                dependency_management_tool=dependency_management_tool,
                middleware=middleware,
            ),
        ).create_chain()
