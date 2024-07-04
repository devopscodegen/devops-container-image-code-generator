"""
This module contains the get_chain function which
returns the find_middleware_chain corresponding to the language and dependency management tool
"""

from devops_code_generator.devops_code_generator_output_parser import (
    DevopsCodeGeneratorOutputParser,
)
from langchain_core.prompts import ChatPromptTemplate

MIDDLEWARES = [
    "apache_tomcat",
    "apache_tomee",
    "eclipse_glassfish",
    "eclipse_jakarta",
    "eclipse_jetty",
    "ibm_openliberty",
    "ibm_redhat_jboss",
    "ibm_redhat_quarkus",
    "ibm_redhat_wildfly",
    "ibm_websphere_liberty",
    "ibm_websphere_traditional",
    "oracle_weblogic",
    "spring_boot_version_2.3.0_and_above",
    "spring_boot_version_less_than_2.3.0",
]


def get_chain(llm):
    """
    This function returns the find_middleware_chain
    corresponding to the language and dependency management tool
    """
    return (
        ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You will be provided with below information
- contents of dependency manifest {dependency_manifest} delimited with ```{dependency_manifest}_begin and ```{dependency_manifest}_end.
- {language} middlewares delimited with ```middlewares_begin and ```middlewares_end.
Your task is to select the correct middleware using only the provided information.
Middleware should be delimited with ```middleware_begin and ```middleware_end.
If more than one {language} middleware are possible, then select the most specific instead of the most generic.
Before selecting the middleware, generate a plan which explains your thinking.
Plan should be delimited with ```plan_begin and ```plan_end.
""",
                ),
                (
                    "human",
                    """```{dependency_manifest}_begin
{dependency_manifest_content}
```{dependency_manifest}_end

```{language}_middlewares_begin
{middlewares}
```{language}_middlewares_end
""",
                ),
            ]
        ).partial(
            middlewares="\n".join(f"- {middleware}" for middleware in MIDDLEWARES)
        )
        | llm
        | DevopsCodeGeneratorOutputParser()
    )
