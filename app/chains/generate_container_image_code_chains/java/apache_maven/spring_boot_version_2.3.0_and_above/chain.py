"""
This module contains the get_chain function which
returns the generate_container_image_code_chain
corresponding to the middleware returned by find_middleware_chain
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


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
