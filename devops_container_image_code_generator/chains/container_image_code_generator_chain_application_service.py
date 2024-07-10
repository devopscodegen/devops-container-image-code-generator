"""
PLACEHOLDER
"""

from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
from .container_image_code_generator_chain import ContainerImageCodeGeneratorChain


class ContainerImageCodeGeneratorChainApplicationService:
    """
    PLACEHOLDER
    """

    def __init__(
        self,
        llm: Runnable = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        ),
    ):
        self.set_llm(llm)

    def get_llm(self) -> Runnable:
        """Get llm"""
        return self.llm

    def set_llm(self, llm: Runnable = None):
        """Set llm"""
        self.llm = llm

    def create_chain(self):
        """
        PLACEHOLDER
        """
        llm = self.get_llm()
        return ContainerImageCodeGeneratorChain(llm=llm).create_chain()

    def __str__(self):
        return self.get_llm()
