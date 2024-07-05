"""
This module contains the get_chain function which
returns the generate_container_image_code_chain
corresponding to the middleware returned by find_middleware_chain
"""

import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


def get_chain(llm, language, dependency_management_tool, middleware):
    """
    This function returns the generate_container_image_code_chain
    corresponding to the middleware returned by find_middleware_chain
    """

    # pylint: disable=R0801
    templates_path = os.path.join(
        "app",
        "chains",
        "generate_container_image_code_chains",
        language,
        dependency_management_tool,
        middleware,
    )

    with open(
        file=os.path.join(templates_path, "Dockerfile.template"),
        mode="r",
        encoding="utf-8",
    ) as file:
        dockerfile_template = file.read()

    dockerfile_template = (
        dockerfile_template.replace("\\", "\\\\").replace("{", "{{").replace("}", "}}")
    )

    entrypoint_script_template_path = os.path.join(
        templates_path, "entrypoint_script.template"
    )

    entrypoint_script_template = ""

    if os.path.isfile(entrypoint_script_template_path):
        with open(
            file=entrypoint_script_template_path, mode="r", encoding="utf-8"
        ) as file:
            entrypoint_script_template = file.read()

        entrypoint_script_template = (
            entrypoint_script_template.replace("\\", "\\\\")
            .replace("{", "{{")
            .replace("}", "}}")
        )

    return (
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
        )
        | llm
        | StrOutputParser()
    )
