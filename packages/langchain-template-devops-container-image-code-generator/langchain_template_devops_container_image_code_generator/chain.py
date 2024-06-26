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

from devops_code_generator.git_source_code_repository import GitSourceCodeRepository
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI


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


llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

find_middleware_chain = {}
find_middleware_chain["java"] = {}
find_middleware_chain["java"]["apache_maven"] = (
    ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "",
            ),
            (
                "human",
                """{dependency_manifest_content}

For above {dependency_manifest}, select the correct {language} middleware out of the below
- apache_tomcat
- apache_tomee
- eclipse_glassfish
- eclipse_jakarta
- eclipse_jetty
- ibm_openliberty
- ibm_redhat_jboss
- ibm_redhat_quarkus
- ibm_redhat_wildfly
- ibm_websphere_liberty
- ibm_websphere_traditional
- oracle_weblogic
- spring_boot_version_2.3.0_and_above
- spring_boot_version_less_than_2.3.0

If more than one middleware are possible, then select the most specific instead of the most generic.
Specify the middleware and nothing else""",
            ),
        ]
    )
    | llm
    | StrOutputParser()
)


def route_to_find_middleware_chain(info: str):
    """
    Routing function which returns the find_middleware_chain
    corresponding to the language and dependency management tool returned by find_middleware_chain
    """
    return find_middleware_chain[info["language"]][info["dependency_management_tool"]]


generate_container_image_code_chain = {}
generate_container_image_code_chain["java"] = {}
generate_container_image_code_chain["java"]["apache_maven"] = {}
generate_container_image_code_chain["java"]["apache_maven"][
    "spring_boot_version_2.3.0_and_above"
] = (
    ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "",
            ),
            (
                "human",
                """{dependency_manifest_content}

For above {dependency_manifest}, use the below Dockerfile template to generate the Dockerfile.
Make the changes required by the {dependency_manifest}. Generate the Dockerfile and nothing else.

FROM eclipse-temurin:21-jdk-jammy as extract

VOLUME /tmp

ARG GID=10001
ARG APPGROUPNAME=appgroup
ARG UID=10001
ARG APPUSERNAME=appuser
ARG APPDIR=/app
ARG APPEXTRACTDIR=$APPDIR/extracted
ARG APPJAR=app.jar

RUN addgroup --gid "${{GID}}" "${{APPGROUPNAME}}" \
&& adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${{UID}}" \
    --gid "${{GID}}" \
    "${{APPUSERNAME}}" \
&& mkdir -m 700 -p "${{APPDIR}}" "${{APPEXTRACTDIR}}" \
&& chown "${{APPUSERNAME}}:${{APPGROUPNAME}}" "${{APPDIR}}" "${{APPEXTRACTDIR}}"

USER $APPUSERNAME:$APPGROUPNAME

WORKDIR $APPDIR

COPY --chown=$APPUSERNAME:$APPGROUPNAME container_image/${{APPJAR}} ./

RUN java -Djarmode=layertools -jar "${{APPJAR}}" extract --destination "${{APPEXTRACTDIR}}"

FROM eclipse-temurin:21-jre-jammy AS final

VOLUME /tmp

ARG GID=10001
ARG APPGROUPNAME=appgroup
ARG UID=10001
ARG APPUSERNAME=appuser
ARG APPDIR=/app
ARG APPEXTRACTDIR=$APPDIR/extracted
ARG APPENTRYPOINT=entrypoint.sh

RUN addgroup --gid "${{GID}}" "${{APPGROUPNAME}}" \
&& adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${{UID}}" \
    --gid "${{GID}}" \
    "${{APPUSERNAME}}" \
&& mkdir -m 700 -p "${{APPDIR}}" \
&& chown "${{APPUSERNAME}}:${{APPGROUPNAME}}" "${{APPDIR}}"

USER $APPUSERNAME:$APPGROUPNAME

WORKDIR $APPDIR

COPY --chown=$APPUSERNAME:$APPGROUPNAME --chmod=700 container_image/$APPENTRYPOINT ./

COPY --from=extract --chown=$APPUSERNAME:$APPGROUPNAME $APPEXTRACTDIR/dependencies/ ./
COPY --from=extract --chown=$APPUSERNAME:$APPGROUPNAME $APPEXTRACTDIR/spring-boot-loader/ ./
COPY --from=extract --chown=$APPUSERNAME:$APPGROUPNAME $APPEXTRACTDIR/snapshot-dependencies/ ./
COPY --from=extract --chown=$APPUSERNAME:$APPGROUPNAME $APPEXTRACTDIR/application/ ./

EXPOSE 8080

ENTRYPOINT ["/app/entrypoint.sh"]""",
            ),
        ]
    )
    | llm
    | StrOutputParser()
)


def route_to_generate_container_image_code_chain(info):
    """
    Routing function which returns the generate_container_image_code_chain
    corresponding to the middleware returned by find_middleware_chain
    """
    return generate_container_image_code_chain[info["language"]][
        info["dependency_management_tool"]
    ][info["middleware"]]


chain = (
    RunnableLambda(runnable_fnd_lang_dep_mfst_dep_mgmt_tool)
    | RunnablePassthrough.assign(
        middleware=RunnableLambda(route_to_find_middleware_chain)
    )
    | RunnableLambda(route_to_generate_container_image_code_chain)
)
