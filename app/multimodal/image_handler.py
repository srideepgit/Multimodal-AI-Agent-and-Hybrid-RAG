import base64

from openai import OpenAI

DESCRIBE_PROMPT = (
    "Describe this image factually and in detail. Transcribe any visible "
    "text verbatim (OCR), including numbers in tables or charts. Do not "
    "guess at information that is not visible in the image."
)


class ImageHandler:
    """
    Converts an image into a grounded text description (caption + OCR)
    using an OpenAI vision-capable chat model.

    The output is plain text, so the rest of the agent (planner, tools,
    response engine) never needs to know an image was involved -- the
    extracted text is simply treated as the user's question / context,
    same as any other text input.
    """

    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def describe(self, image_bytes: bytes, mime_type: str = "image/png") -> str:
        if not image_bytes:
            raise ValueError("No image data provided.")

        encoded = base64.b64encode(image_bytes).decode("utf-8")

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": DESCRIBE_PROMPT,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{encoded}",
                            },
                        },
                    ],
                }
            ],
        )

        description = response.choices[0].message.content

        if not description or not description.strip():
            raise ValueError("The vision model returned an empty description.")

        return description.strip()
