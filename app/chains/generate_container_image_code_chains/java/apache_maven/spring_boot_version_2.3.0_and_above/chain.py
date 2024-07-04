"""
This module contains the get_chain function which
returns the generate_container_image_code_chain
corresponding to the middleware returned by find_middleware_chain
"""

from devops_code_generator.devops_code_generator_output_parser import (
    DevopsCodeGeneratorOutputParser,
)
from langchain_core.prompts import ChatPromptTemplate


def get_chain(llm):
    """
    This function returns the generate_container_image_code_chain
    corresponding to the middleware returned by find_middleware_chain
    """
    return (
        ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You will be provided with below information
- contents of dependency manifest {dependency_manifest} delimited with ```{dependency_manifest}_begin and ```{dependency_manifest}_end.
- Dockerfile template delimited with ```Dockerfile_template_begin and ```Dockerfile_template_end.
- entrypoint script template delimited with ```entrypoint_script_template_begin and ```entrypoint_script_template_end.
Your task is to generate the Dockerfile and entrypoint script using only the provided information.
Dockerfile should be delimted with delimited with ```Dockerfile_begin and ```Dockerfile_end.
entrypoint script should be delimited with ```entrypoint_script_begin and ```entrypoint_script_end.
Make the changes required by the dependency manifest {dependency_manifest}.
Before generating the Dockerfile and entrypoint script, generate a plan which explains your thinking.
Plan should be delimited with ```plan_begin and ```plan_end.
""",
                ),
                (
                    "human",
                    """```{dependency_manifest}_begin
{dependency_manifest_content}
```{dependency_manifest}_end

```Dockerfile_template_begin
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

ENTRYPOINT ["/app/entrypoint.sh"]
```Dockerfile_template_end

```entrypoint_script_template_begin
#!/bin/sh

cd /app

exec java ${{JAVA_OPTS}} org.springframework.boot.loader.launch.JarLauncher ${{@}}
```entrypoint_script_template_end
""",
                ),
            ]
        )
        | llm
        | DevopsCodeGeneratorOutputParser()
    )
