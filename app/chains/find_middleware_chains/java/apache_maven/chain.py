"""
This module contains the get_chain function which
returns the find_middleware_chain corresponding to the language and dependency management tool
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def get_chain(llm):
    """
    This function returns the gfind_middleware_chain
    corresponding to the language and dependency management tool
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
