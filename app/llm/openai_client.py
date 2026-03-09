from openai import OpenAI

from app.llm.base import BaseLLM


class OpenAIClient(BaseLLM):

    def __init__(
        self,
        api_key: str,
        model: str,
    ):

        self.client = OpenAI(
            api_key=api_key,
        )

        self.model = model

    def invoke(
        self,
        prompt: str,
    ) -> str:

        response = self.client.chat.completions.create(

            model=self.model,

            messages=[

                {
                    "role":"user",
                    "content":prompt,
                }

            ]
        )

        return response.choices[0].message.content