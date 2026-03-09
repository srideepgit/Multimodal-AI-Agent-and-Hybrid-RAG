import logging

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    WebSocket,
)

from app.api.dependencies import (
    get_ai_service,
    get_audio_handler,
    get_image_handler,
    get_video_handler,
    get_voice_session,
)
from app.api.schemas import ChatRequest, ChatResponse, MultimodalChatResponse
from app.core.config import get_settings
from app.multimodal.audio_handler import AudioHandler
from app.multimodal.image_handler import ImageHandler
from app.multimodal.video_handler import VideoHandler
from app.services.ai_service import AIService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    service: AIService = Depends(get_ai_service),
):

    try:
        response = service.chat(request.question)

    except ValueError as exc:
        # Raised by tools for bad/unsafe input (e.g. a malformed
        # calculator expression or a non-SELECT SQL query).
        logger.warning("Rejected chat request: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    except Exception as exc:
        logger.exception("Unhandled error while answering chat request")
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while generating the answer.",
        ) from exc

    return response


# -----------------------------------------------------------------
# Multimodal endpoints
#
# Each endpoint follows the same shape: read the uploaded file,
# convert it to text with the relevant handler, optionally combine
# it with a user-supplied question, then run it through the exact
# same agent graph that /chat uses. No tool/planner/response code
# needs to know a non-text modality was ever involved.
# -----------------------------------------------------------------


async def _read_upload(file: UploadFile, max_size_mb: int) -> bytes:
    data = await file.read()

    if len(data) > max_size_mb * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds the {max_size_mb}MB upload limit.",
        )

    if not data:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    return data


def _combine_question(user_question: str | None, extracted_text: str, label: str) -> str:
    if user_question and user_question.strip():
        return (
            f"{user_question.strip()}\n\n"
            f"[Attached {label} content]:\n{extracted_text}"
        )

    return extracted_text


def _run_chat(
    service: AIService,
    question: str,
    modality: str,
    extracted_text: str,
) -> MultimodalChatResponse:

    result = service.chat(question)

    return MultimodalChatResponse(
        answer=result["answer"],
        sources=result["sources"],
        confidence=result["confidence"],
        modality=modality,
        extracted_text=extracted_text,
    )


@router.post(
    "/chat/image",
    response_model=MultimodalChatResponse,
)
async def chat_image(
    file: UploadFile = File(...),
    question: str | None = Form(default=None),
    service: AIService = Depends(get_ai_service),
    image_handler: ImageHandler = Depends(get_image_handler),
):

    settings = get_settings()
    data = await _read_upload(file, settings.max_upload_size_mb)

    try:
        extracted_text = image_handler.describe(
            data,
            mime_type=file.content_type or "image/png",
        )

        combined_question = _combine_question(question, extracted_text, "image")

        return _run_chat(service, combined_question, "image", extracted_text)

    except ValueError as exc:
        logger.warning("Rejected image chat request: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    except Exception as exc:
        logger.exception("Unhandled error while answering image chat request")
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while processing the image.",
        ) from exc


@router.post(
    "/chat/audio",
    response_model=MultimodalChatResponse,
)
async def chat_audio(
    file: UploadFile = File(...),
    question: str | None = Form(default=None),
    service: AIService = Depends(get_ai_service),
    audio_handler: AudioHandler = Depends(get_audio_handler),
):

    settings = get_settings()
    data = await _read_upload(file, settings.max_upload_size_mb)

    try:
        extracted_text = audio_handler.transcribe(
            data,
            filename=file.filename or "audio.wav",
        )

        if not extracted_text:
            raise ValueError("Could not hear any speech in that audio file.")

        combined_question = _combine_question(question, extracted_text, "audio")

        return _run_chat(service, combined_question, "audio", extracted_text)

    except ValueError as exc:
        logger.warning("Rejected audio chat request: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    except Exception as exc:
        logger.exception("Unhandled error while answering audio chat request")
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while processing the audio.",
        ) from exc


@router.post(
    "/chat/video",
    response_model=MultimodalChatResponse,
)
async def chat_video(
    file: UploadFile = File(...),
    question: str | None = Form(default=None),
    service: AIService = Depends(get_ai_service),
    video_handler: VideoHandler = Depends(get_video_handler),
):

    settings = get_settings()
    data = await _read_upload(file, settings.max_upload_size_mb)

    try:
        extracted_text = video_handler.process(
            data,
            filename=file.filename or "video.mp4",
        )

        combined_question = _combine_question(question, extracted_text, "video")

        return _run_chat(service, combined_question, "video", extracted_text)

    except ValueError as exc:
        logger.warning("Rejected video chat request: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    except RuntimeError as exc:
        # ffmpeg missing from the environment.
        logger.error("Video processing unavailable: %s", exc)
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    except Exception as exc:
        logger.exception("Unhandled error while answering video chat request")
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while processing the video.",
        ) from exc


@router.websocket("/ws/voice")
async def chat_voice(websocket: WebSocket):
    """
    Realtime, push-to-talk voice endpoint.

    Send one binary WebSocket message per utterance (full audio clip).
    Receive back a JSON text message with the transcript + answer,
    followed by a binary message with the synthesized speech reply.
    See app.multimodal.voice_realtime.VoiceSession for the protocol.
    """

    session = get_voice_session()

    await session.run(websocket)
