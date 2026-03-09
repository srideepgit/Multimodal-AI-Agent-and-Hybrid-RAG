from unittest.mock import MagicMock, patch

import pytest

from app.multimodal.image_handler import ImageHandler


def _make_handler(response_text="A whiteboard with the text 'Q3 revenue: $4.2M'."):
    with patch("app.multimodal.image_handler.OpenAI") as mock_openai_cls:
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client

        completion = MagicMock()
        completion.choices = [MagicMock(message=MagicMock(content=response_text))]
        mock_client.chat.completions.create.return_value = completion

        handler = ImageHandler(api_key="test-key", model="gpt-4o-mini")

    return handler, mock_client


def test_describe_returns_model_text():
    handler, mock_client = _make_handler()

    result = handler.describe(b"fake-image-bytes", mime_type="image/png")

    assert result == "A whiteboard with the text 'Q3 revenue: $4.2M'."
    mock_client.chat.completions.create.assert_called_once()


def test_describe_sends_base64_data_url():
    handler, mock_client = _make_handler()

    handler.describe(b"fake-image-bytes", mime_type="image/jpeg")

    call_kwargs = mock_client.chat.completions.create.call_args.kwargs
    content = call_kwargs["messages"][0]["content"]
    image_block = next(block for block in content if block["type"] == "image_url")

    assert image_block["image_url"]["url"].startswith("data:image/jpeg;base64,")


def test_describe_rejects_empty_input():
    handler, _ = _make_handler()

    with pytest.raises(ValueError):
        handler.describe(b"")


def test_describe_rejects_empty_model_output():
    handler, _ = _make_handler(response_text="")

    with pytest.raises(ValueError):
        handler.describe(b"fake-image-bytes")
