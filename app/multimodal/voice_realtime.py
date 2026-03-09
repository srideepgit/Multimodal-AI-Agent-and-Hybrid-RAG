import json
import logging

from fastapi import WebSocket, WebSocketDisconnect

from app.multimodal.audio_handler import AudioHandler
from app.services.ai_service import AIService

logger = logging.getLogger(__name__)


class VoiceSession:
    """
    Push-to-talk realtime voice loop over a WebSocket.

    Protocol (repeats per turn, until the client disconnects):

      1. Client sends ONE binary WebSocket message containing a complete
         utterance's raw audio bytes (e.g. a recorded clip, not a live
         byte stream).
      2. Server:
           a. transcribes it with Whisper (``AudioHandler.transcribe``)
           b. runs the transcript through the same LangGraph agent used
              by ``POST /chat``
           c. sends back a JSON text message describing the answer:
              {"type": "answer", "transcript": ..., "text": ..., "confidence": ...}
           d. sends back a binary message containing synthesized speech
              (TTS) for that answer.

    This is intentionally a turn-based loop rather than token-level
    audio streaming -- it gives a real speech-in/speech-out experience
    with a small, easy-to-reason-about surface area. True continuous
    streaming (interrupting mid-sentence, partial transcripts) would
    need a persistent duplex model session and is left as a roadmap
    item (see README).
    """

    def __init__(self, audio_handler: AudioHandler, ai_service: AIService):
        self.audio_handler = audio_handler
        self.ai_service = ai_service

    async def run(self, websocket: WebSocket):
        await websocket.accept()

        try:
            while True:
                audio_bytes = await websocket.receive_bytes()

                try:
                    transcript = self.audio_handler.transcribe(
                        audio_bytes,
                        filename="utterance.wav",
                    )

                    if not transcript:
                        await websocket.send_text(
                            json.dumps(
                                {
                                    "type": "error",
                                    "detail": "Could not hear any speech in that clip.",
                                }
                            )
                        )
                        continue

                    result = self.ai_service.chat(transcript)

                    await websocket.send_text(
                        json.dumps(
                            {
                                "type": "answer",
                                "transcript": transcript,
                                "text": result["answer"],
                                "confidence": result["confidence"],
                            }
                        )
                    )

                    speech = self.audio_handler.synthesize(result["answer"])

                    await websocket.send_bytes(speech)

                except ValueError as exc:
                    await websocket.send_text(
                        json.dumps({"type": "error", "detail": str(exc)})
                    )

        except WebSocketDisconnect:
            logger.info("Voice session disconnected.")
