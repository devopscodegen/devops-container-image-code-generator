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

GenAI Application which uses Langchain and source code repository files, such as dependency manifests, to generate container image code like Dockerfile and entrypoint script.

## Approach
- Developers write source code, unit test code, dependency manifests like pom.xml, package.json, requirements.txt and static assets on their machine and checkin to the source code repository
- devops-container-image-code-generator uses devops-code-generator package to checkout the source code repository and identify language, dependency manifest and dependency management tool from the dependency manifest checked into the source code repository
- It then uses langchain genai middleware chain to identify the middleware from the dependency manifest
- It then uses routing function to route to the langchain genai subchain corresponding to the identified middleware to generate container image code like Dockerfile and entrypoint script for the source code repository.

This approach shall be used to generate other DevOps code like pipeline code, infrastructure code, database code, deployment code, container deployment code, etc.

## Templates
Currently, templates exist for below language, dependency management tool and middleware combinations
- language : java
    - dependency management tool : apache_maven
        - middlewares : apache_tomcat, spring_boot_version_2.3.0_and_above and spring_boot_version_less_than_2.3.0
- language : python
    - dependency management tool : poetry
        - middlewares : langserve

## Future Work
- Add templates for other language, dependency management tool and middleware combinations.
- Use other files in the source code repository like README.md, etc. to update the generated container image code.
- Use low level design document and images to update the generated container image code.

## Environment Setup

Set the following environment variable to access OpenAI GPT4-o model
```shell
OPENAI_API_KEY='XXX'
```

Set the following environment variable to change the logging level from default WARNING to INFO
```shell
DEVOPS_CONTAINER_IMAGE_CODE_GENERATOR_LOG_LEVEL=info
```

System Git should have access to the input git source code repository.

## Usage

To test this application, do the following steps

- Install poetry ( python dependency management tool which internally uses pip ) using [https://python-poetry.org/docs/#installing-with-the-official-installer](https://python-poetry.org/docs/#installing-with-the-official-installer)
- Clone the git repository.
- Run command ```poetry install --with dev``` to install required dependencies.
- Run command ```OTEL_SERVICE_NAME= langchain serve``` to start the application.
- Open playground in Browser at [http://127.0.0.1:8000/devops-container-image-code-generator/playground/](http://127.0.0.1:8000/devops-container-image-code-generator/playground/) and provide ```https://github.com/spring-projects/spring-petclinic``` as input.
 It will output the reasoning, Dockerfile and entrypoint script for this spring boot middleware application component. You can click on Intermediate Steps to check the intermediate steps taken by the Langchain chain.
- Again Open playground at [http://127.0.0.1:8000/devops-container-image-code-generator/playground/](http://127.0.0.1:8000/devops-container-image-code-generator/playground/) and provide ```https://github.com/spring-petclinic/spring-framework-petclinic```as input. It will output the reasoning and Dockerfile for this apache tomcat middleware application component. You can click on Intermediate Steps to check the intermediate steps taken by the Langchain chain.
- Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in browser to try all OpenAPI specifications
- Access the api from code with:
```python
from langserve.client import RemoteRunnable
runnable = RemoteRunnable("http://127.0.0.1:8000")
```

## Opentelemetry autoinstrumentation (Traces, Metrics and Logs)

### Set the following environment variables to use Opentelemetry autoinstrumentation

```shell
OTEL_SERVICE_NAME='devops-container-image-code-generator:<version>'
OTEL_TRACES_EXPORTER=console
OTEL_METRICS_EXPORTER=console
OTEL_LOGS_EXPORTER=console
OTEL_PYTHON_EXCLUDED_URLS="client/.*/info,healthcheck"
OTEL_PYTHON_LOG_CORRELATION=true
OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
OTEL_PYTHON_DISABLED_INSTRUMENTATIONS="asyncio"
OTEL_PYTHON_LOG_LEVEL=${DEVOPS_CONTAINER_IMAGE_CODE_GENERATOR_LOG_LEVEL}
```

### Apply the below Workaround for Opentelemetry autoinstrumentation to work with uvicorn

Add below code as first line after documentation in the function subprocess_started in file site-packages/uvicorn/_subprocess.py
```
    if os.getenv('OTEL_SERVICE_NAME'):
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
    if os.getenv('OTEL_SERVICE_NAME'):
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
```shell
opentelemetry-instrument langchain serve
```

### Run below command if environment variable OTEL_SERVICE_NAME is set and you do not want to use Opentelemetey autoinstrumentation
```shell
OTEL_SERVICE_NAME= langchain serve
```

## OpenAI GPT4-o Prompt Engineering Tactics

| Tactic | Status | Comment |
| --- | --- | --- |
| Include details in your query to get more relevant answers | Done | Added complete instructions like "Generate the Dockerfile and entrypoint script and nothing else." so that model does not guess what we mean |
| Ask the model to adopt a persona | Done | Added system message |
| Use delimiters to clearly indicate distinct parts of the input | Done | All provided templates are delimited with \`\`\`_begin and \`\`\`_end
| Specify the steps required to complete a task | Done | Used Langchain chain to divide the task of generating Dockerfile and entrypoint script into 2 steps 1. Find Middleware 2. Generate Dockerfile and entrypoint script |
| Provide examples | To do | Not provided |
| Specify the desired length of the output | Not required | Reason - we need the model to generate complete Dockerfile and entrypoint script from the template. |
| Instruct the model to answer using a reference text | Done | Provided templates for Dockerfile and entrypoint script |
| Instruct the model to answer with citations from a reference text | Not required | Reason - we need the model to only generate Dockerfile and entrypoint script from the template. |
Use intent classification to identify the most relevant instructions for a user query | Done | Used Langchain chain to divide the task of generating Dockerfile and entrypoint script into 2 steps 1. Find Middleware 2. Generate Dockerfile and entrypoint script |
| For dialogue applications that require very long conversations, summarize or filter previous dialogue | Not required | Reason - we are not creating a dialogue application as of now. |
| Summarize long documents piecewise and construct a full summary recursively | To do | Need to check whether we need to provide other files to the model to improve the generated Dockerfile and entrypoint script. |
| Instruct the model to work out its own solution before rushing to a conclusion | Not required | Reason - we are not checking any solution |
| Use inner monologue or a sequence of queries to hide the model's reasoning process | Done | Added following lines to the prompt. Before selecting the middleware, generate a plan which explains your thinking. Before generating the Dockerfile and entrypoint script, generate a plan which explains your thinking. Plan should be delimited with \`\`\`plan_begin and \`\`\`plan_end. |
| Ask the model if it missed anything on previous passes | To do | Need to check if we need to add this to the chain
| Use embeddings-based search to implement efficient knowledge retrieval | To do |
| Use code execution to perform more accurate calculations or call external APIs | To do |
| Give the model access to specific functions | To do | Need to call Dockerfile and entrypoint script linting to check if there are any problems in the generated files. If there are then provide the errors to the chain and regenerate the Dockerfile and entrypoint script. RetryOutputParser |
| Evaluate model outputs with reference to gold-standard answers | To do | Need to add test cases and use another LLM chain to evaluate if the generated Dockerfile and entrypoint_script matches the expected test output |

## Design Notes
- \`\`\` cannot be used as end delimiter by itself since it will need to be escaped if it is part of the actual generated text.
- PydanticOutputParser cannot be used since it does not support streaming which is required in playground (astream_log)
- JsonOutputParser cannot be used because we will have to escape ""
- Created DevopsCodeGeneratorOutputParser Custom Output Parser. Copy of JsonOutputParser like base class is BaseCumulativeTransformOutputParser.
- Use existing langchain code as template instead of just using the documentation which may not be updated
- Used .partial method of ChatPromptTemplate to create middlewares markdown string from MIDDLEWARES list.
