[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![PyPI - Version](https://img.shields.io/pypi/v/devops-container-image-code-generator)]()
[![PyPI - Downloads](https://img.shields.io/pypi/dm/devops-container-image-code-generator)](https://pypistats.org/packages/devops-container-image-code-generator)
[![PyPI - License](https://img.shields.io/pypi/l/devops-container-image-code-generator)]()
[![PyPI - Status](https://img.shields.io/pypi/status/devops-container-image-code-generator)]()
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/devops-container-image-code-generator)]()

# devops-container-image-code-generator

This template utilizes source code repository files, such as dependency manifests, to generate container image code like Dockerfile and entrypoint shell script using LangChain GenAI. 

## Approach
- Developers write source code, unit test code, dependency manifests like pom.xml, package.json, requirements.txt and static assets on their machine and checkin to the source code repository
- devops-container-image-code-generator uses devops-code-generator package to checkout the source code repository and identify language, dependency manifest and dependency management tool from the dependency manifest checked into the source code repository
- It then uses langchain genai middleware chain to identify the middleware from the dependency manifest
- It then uses routing function to route to the langchain genai subchain corresponding to the identified middleware to generate container image code like Dockerfile and entrypoint shell script for the source code repository.

This approach shall be used to generate other DevOps code like pipeline code, infrastructure code, database code, deployment code, container deployment code, etc.

## Constraints
Currently only works for below constraints
- language : java
- dependency management tool : apache_maven 
- middleware : spring_boot_version_2.3.0_and_above middleware.

## Future Work
- Add templates for other languages, dependency management tools and middlewares.
- Use other files in the source code repository like README.md, etc. to update the generated container image code.
- Use low level design document and images to update the generated container image code.

## Environment Setup

It uses OpenAI gpt-4o Model. Set the `OPENAI_API_KEY` environment variable to access the OpenAI models.
System Git should have access to the input git source code repository.

## Usage

To use this package, you should first have the LangChain CLI installed:

```shell
pip install -U langchain-cli
```

To create a new LangChain project and install this as the only package, you can do:

```shell
langchain app new my-app --package devops-container-image-code-generator
```

If you want to add this to an existing project, you can just run:

```shell
langchain app add devops-container-image-code-generator
```

And add the following code to your `server.py` file:
```python
from devops_container_image_code_generator import chain as devops_container_image_code_generator_chain

add_routes(app, devops_container_image_code_generator_chain, path="/devops-container-image-code-generator")
```

(Optional) Let's now configure LangSmith. 
LangSmith will help us trace, monitor and debug LangChain applications. 
You can sign up for LangSmith [here](https://smith.langchain.com/). 
If you don't have access, you can skip this section


```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # if not specified, defaults to "default"
```

If you are inside this directory, then you can spin up a LangServe instance directly by:

```shell
langchain serve
```

This will start the FastAPI app with a server is running locally at 
[http://localhost:8000](http://localhost:8000)

We can see all templates at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
We can access the playground at [http://127.0.0.1:8000/devops-container-image-code-generator/playground](http://127.0.0.1:8000/devops-container-image-code-generator/playground)  

We can access the template from code with:

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://localhost:8000/devops-container-image-code-generator")
```