from app.llm.openai_client import OpenAIClient


class LLMFactory:

    @staticmethod
    def create(
        provider: str,
        api_key: str,
        model: str,
    ):

        provider = provider.lower()

        if provider == "openai":

            return OpenAIClient(
                api_key,
                model,
            )

        raise ValueError(
            "Unsupported provider"
        )