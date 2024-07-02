"""
This module utilizes source code repository files, such as dependency manifests,
to generate container image code like Dockerfile and entrypoint shell script using LangChain GenAI.

# Approach
- Developers write source code, unit test code,
dependency manifests like pom.xml, package.json, requirements.txt and static assets
on their machine and checkin to the source code repository
- devops-container-image-code-generator uses devops-code-generator package
to checkout the source code repository
and identify language, dependency manifest and dependency management tool
from the dependency manifest checked into the source code repository
- It then uses langchain genai middleware chain
to identify the middleware from the dependency manifest
- It then uses routing function to route to the langchain genai subchain
corresponding to the identified middleware
to generate container image code like Dockerfile and entrypoint shell script
for the source code repository.

This approach shall be used to generate other DevOps code
like pipeline code, infrastructure code, database code,
deployment code, container deployment code, etc.

# Constraints
Currently only works for below constraints
- language : java
- dependency management tool : apache_maven
- middleware : spring_boot_version_2.3.0_and_above middleware.

# Future Work
- Add prompt templates for other languages, dependency management tools and middlewares.
- Use other files in the source code repository like README.md, etc.
to update the generated container image code.
- Use low level design document and images to update the generated container image code.

"""

import importlib
import os
from devops_code_generator.git_source_code_repository import GitSourceCodeRepository
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI


def import_module(name, path):
    """
    This function dynamically imports a Python module from a given file path.
    """
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def runnable_fnd_lang_dep_mfst_dep_mgmt_tool(text: str):
    """
    Function which takes git source code repository as input and
    returns the language, dependency manifest, dependency manifest content and
    dependency management tool.
    """
    git_source_code_repository = GitSourceCodeRepository(
        path=None, url=text, branch="main"
    )
    git_source_code_repository.checkout_branch()
    git_source_code_repository.fnd_lang_dep_mfst_dep_mgmt_tool()
    return {
        "language": git_source_code_repository.get_language(),
        "dependency_manifest": git_source_code_repository.get_dependency_manifest(),
        "dependency_management_tool": git_source_code_repository.get_dependency_management_tool(),
        "dependency_manifest_content": git_source_code_repository.get_dependency_manifest_content(),
    }


def route_to_find_middleware_chain(info: dict):
    """
    Routing function which returns the find_middleware_chain
    corresponding to the language and dependency management tool
    """
    module_name = "find_middleware_chain_module"
    module_path = os.path.join(
        "app",
        "chains",
        "find_middleware_chains",
        info["language"],
        info["dependency_management_tool"],
        "chain.py",
    )
    find_middleware_chain_module = import_module(name=module_name, path=module_path)
    return find_middleware_chain_module.get_chain(llm)


def route_to_generate_container_image_code_chain(info: dict):
    """
    Routing function which returns the generate_container_image_code_chain
    corresponding to the middleware returned by find_middleware_chain
    """
    module_name = "generate_container_image_code_chain_module"
    module_path = os.path.join(
        "app",
        "chains",
        "generate_container_image_code_chains",
        info["language"],
        info["dependency_management_tool"],
        info["middleware"],
        "chain.py",
    )
    generate_container_image_code_chain_module = import_module(
        name=module_name, path=module_path
    )
    return generate_container_image_code_chain_module.get_chain(llm)


llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

chain = (
    RunnableLambda(runnable_fnd_lang_dep_mfst_dep_mgmt_tool)
    | RunnablePassthrough.assign(
        middleware=RunnableLambda(route_to_find_middleware_chain)
    )
    | RunnableLambda(route_to_generate_container_image_code_chain)
)
