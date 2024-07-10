"""
PLACEHOLDER
"""

from importlib.resources import files
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from devopscodegen_common.repositories import SourceCodeRepository


class ContainerImageCodeGeneratorChainForMiddleware:
    """
    PLACEHOLDER
    """

    # pylint: disable=R0913
    def __init__(
        self,
        llm: Runnable = None,
        source_code_repository: SourceCodeRepository = None,
        chain=None,
        templates_package: str = "devops_container_image_code_generator.templates.container_image_code",
    ):
        self.set_llm(llm)
        self.set_source_code_repository(source_code_repository)
        self.set_chain(chain)
        self.set_templates_package(templates_package)

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

    def get_templates_package(self) -> str:
        """Get templates_package"""
        return self.templates_package

    def set_templates_package(self, templates_package: str = None):
        """Set chain"""
        self.templates_package = templates_package

    def create_chain(self) -> Runnable:
        """Create container image code chain"""
        llm = self.get_llm()
        language = self.get_source_code_repository().get_language()
        dependency_management_tool = (
            self.get_source_code_repository().get_dependency_management_tool()
        )
        middleware = self.get_source_code_repository().get_middleware()
        templates_package = self.get_templates_package()

        dockerfile_template = (
            files(templates_package)
            .joinpath(
                language, dependency_management_tool, middleware, "Dockerfile.template"
            )
            .read_text(encoding="utf-8")
            .replace("\\", "\\\\")
            .replace("{", "{{")
            .replace("}", "}}")
        )

        entrypoint_script_template = ""
        try:
            entrypoint_script_template = (
                files(templates_package)
                .joinpath(
                    language,
                    dependency_management_tool,
                    middleware,
                    "entrypoint_script.template",
                )
                .read_text(encoding="utf-8")
                .replace("\\", "\\\\")
                .replace("{", "{{")
                .replace("}", "}}")
            )
        except FileNotFoundError:
            print("Optional entrypoint script template not found.")

        prompt_append = ""
        try:
            prompt_append = (
                files(templates_package)
                .joinpath(
                    language,
                    dependency_management_tool,
                    middleware,
                    "prompt_append.txt",
                )
                .read_text(encoding="utf-8")
                .replace("\\", "\\\\")
                .replace("{", "{{")
                .replace("}", "}}")
            )
        except FileNotFoundError:
            print("Optional prompt append text file not found.")

        chain = (
            ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """You will be provided with below information
- contents of dependency manifest {dependency_manifest} enclosed within ```{dependency_manifest}_begin and ```{dependency_manifest}_end delimiters.
- Dockerfile template enclosed within ```Dockerfile_template_begin and ```Dockerfile_template_end delimiters.
- entrypoint script template enclosed within ```entrypoint_script_template_begin and ```entrypoint_script_template_end delimiters.
Your task is to generate the Dockerfile and entrypoint script using only the provided information.
Dockerfile should be enclosed within ```Dockerfile_begin and ```Dockerfile_end delimiters.
Generate entrypoint script only if entrypoint script template is provided and not empty. entrypoint script should be enclosed within ```entrypoint_script_begin and ```entrypoint_script_end delimiters.
Make the changes required by the dependency manifest {dependency_manifest}.
This generated Dockerfile and entrypoint script will be used in the container image build stage of CI/CD pipeline.
CI/CD pipeline will copy all the required build artifacts to the directories required by the Dockerfile and entrypoint script in the earlier stages.
Before generating the Dockerfile and entrypoint script, explain your reasoning.
Your reasoning should be enclosed within ```reasoning_begin and ```reasoning_end delimiters.
{prompt_append}
""",
                    ),
                    (
                        "human",
                        """```{dependency_manifest}_begin
    {dependency_manifest_content}
    ```{dependency_manifest}_end delimiters

    ```Dockerfile_template_begin
    {dockerfile_template}
    ```Dockerfile_template_end delimiters

    ```entrypoint_script_template_begin
    {entrypoint_script_template}
    ```entrypoint_script_template_end delimiters
    """,
                    ),
                ]
            ).partial(
                dockerfile_template=dockerfile_template,
                entrypoint_script_template=entrypoint_script_template,
                prompt_append=prompt_append,
            )
            | llm
            | StrOutputParser()
        ).with_config(run_name="generate_container_image_code_chain")
        self.set_chain(chain)
        return chain
