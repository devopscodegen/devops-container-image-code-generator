[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![PyPI - Version](https://img.shields.io/pypi/v/devops-container-image-code-generator)]()
[![PyPI - Downloads](https://img.shields.io/pypi/dm/devops-container-image-code-generator)](https://pypistats.org/packages/devops-container-image-code-generator)
[![PyPI - License](https://img.shields.io/pypi/l/devops-container-image-code-generator)]()
[![PyPI - Status](https://img.shields.io/pypi/status/devops-container-image-code-generator)]()
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/devops-container-image-code-generator)]()
[![GitHub Repo stars](https://img.shields.io/github/stars/devops-code-generators/devops-container-image-code-generator)
](https://star-history.com/#devops-code-generators/devops-container-image-code-generator)
[![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/devops-code-generators/devops-container-image-code-generator)](https://github.com/devops-code-generators/devops-container-image-code-generator/issues)

# devops-container-image-code-generator

Utilizes source code repository files, such as dependency manifests, to generate container image code like Dockerfile and entrypoint shell script using LangChain GenAI.

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

Then spin up a LangServe instance directly by:

```shell
langchain serve
```

This will start the FastAPI app with a server is running locally at
[http://127.0.0.1:8000](http://127.0.0.1:8000)

We can see all openapi specification at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
We can access the playground at [http://127.0.0.1:8000/playground](http://127.0.0.1:8000/playground)

We can access the api from code with:

```python
from langserve.client import RemoteRunnable

runnable = RemoteRunnable("http://127.0.0.1:8000")
```

## Opentelemetry

### Workaround for Opentelemetry autoinstrumentation to work with uvicorn
https://github.com/open-telemetry/opentelemetry-python-contrib/issues/385#issuecomment-808794045

Add below code as first line after documentation in the function subprocess_started in file site-packages/uvicorn/_subprocess.py
```
from opentelemetry.instrumentation.auto_instrumentation import sitecustomize
```
For Example :
```
def subprocess_started(
    config: Config,
    target: Callable[..., None],
    sockets: List[socket],
    stdin_fileno: Optional[int],
) -> None:
    """
    Called when the child process starts.

    * config - The Uvicorn configuration instance.
    * target - A callable that accepts a list of sockets. In practice this will
               be the `Server.run()` method.
    * sockets - A list of sockets to pass to the server. Sockets are bound once
                by the parent process, and then passed to the child processes.
    * stdin_fileno - The file number of sys.stdin, so that it can be reattached
                     to the child process.
    """
    from opentelemetry.instrumentation.auto_instrumentation import sitecustomize
    # Re-open stdin.
    if stdin_fileno is not None:
        sys.stdin = os.fdopen(stdin_fileno)

    # Logging needs to be setup again for each child.
    config.configure_logging()

    # Now we can call into `Server.run(sockets=sockets)`
    target(sockets=sockets)
```

### Run below command to use Opentelemetry autoinstrumentation
```
opentelemetry-instrument langchain serve
```
