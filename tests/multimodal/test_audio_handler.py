from unittest.mock import MagicMock, patch

import pytest

from app.multimodal.audio_handler import AudioHandler


def _make_handler():
    with patch("app.multimodal.audio_handler.OpenAI") as mock_openai_cls:
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client

        handler = AudioHandler(
            api_key="test-key",
            stt_model="whisper-1",
            tts_model="tts-1",
            tts_voice="alloy",
        )

    return handler, mock_client


def test_transcribe_returns_stripped_text():
    handler, mock_client = _make_handler()
    mock_client.audio.transcriptions.create.return_value = MagicMock(
        text="  what is the leave policy?  "
    )

    result = handler.transcribe(b"fake-audio-bytes", filename="clip.wav")

    assert result == "what is the leave policy?"
    mock_client.audio.transcriptions.create.assert_called_once()


def test_transcribe_rejects_empty_input():
    handler, _ = _make_handler()

    with pytest.raises(ValueError):
        handler.transcribe(b"")


def test_synthesize_returns_bytes():
    handler, mock_client = _make_handler()
    mock_response = MagicMock()
    mock_response.read.return_value = b"fake-mp3-bytes"
    mock_client.audio.speech.create.return_value = mock_response

    result = handler.synthesize("Employees get 20 annual leave days.")

    assert result == b"fake-mp3-bytes"
    mock_client.audio.speech.create.assert_called_once_with(
        model="tts-1",
        voice="alloy",
        input="Employees get 20 annual leave days.",
    )


def test_synthesize_rejects_empty_text():
    handler, _ = _make_handler()

    with pytest.raises(ValueError):
        handler.synthesize("")
