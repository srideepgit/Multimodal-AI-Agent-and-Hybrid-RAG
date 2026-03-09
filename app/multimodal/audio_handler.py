import io

from openai import OpenAI


class AudioHandler:
    """
    Speech-to-text (transcription) and text-to-speech (synthesis)
    wrapper around the OpenAI audio APIs.
    """

    def __init__(
        self,
        api_key: str,
        stt_model: str,
        tts_model: str,
        tts_voice: str = "alloy",
    ):
        self.client = OpenAI(api_key=api_key)
        self.stt_model = stt_model
        self.tts_model = tts_model
        self.tts_voice = tts_voice

    def transcribe(self, audio_bytes: bytes, filename: str = "audio.wav") -> str:
        """
        Transcribe raw audio bytes into text.
        """

        if not audio_bytes:
            raise ValueError("No audio data provided.")

        audio_file = io.BytesIO(audio_bytes)
        # The OpenAI SDK infers content type from this attribute name.
        audio_file.name = filename

        transcript = self.client.audio.transcriptions.create(
            model=self.stt_model,
            file=audio_file,
        )

        text = getattr(transcript, "text", "") or ""

        return text.strip()

    def synthesize(self, text: str) -> bytes:
        """
        Convert text into spoken audio bytes (MP3).
        """

        if not text or not text.strip():
            raise ValueError("No text provided for speech synthesis.")

        response = self.client.audio.speech.create(
            model=self.tts_model,
            voice=self.tts_voice,
            input=text,
        )

        return response.read()
