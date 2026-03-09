from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """
    Base interface for all LLM providers.
    """

    @abstractmethod
    def invoke(
        self,
        prompt: str,
    ) -> str:
        pass