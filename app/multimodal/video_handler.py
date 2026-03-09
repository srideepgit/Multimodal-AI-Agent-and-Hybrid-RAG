import os
import shutil
import subprocess
import tempfile

from app.multimodal.audio_handler import AudioHandler
from app.multimodal.image_handler import ImageHandler


class VideoHandler:
    """
    Turns a video file into text by combining two existing handlers:

      1. Sample a handful of frames at a fixed interval and describe
         each one with ``ImageHandler`` (vision captioning + OCR).
      2. Extract the audio track and transcribe it with
         ``AudioHandler`` (Whisper).

    The two results are concatenated into a single block of text that
    feeds into the same LangGraph pipeline as any other question --
    no separate "video" tool is needed downstream.

    Requires the ``ffmpeg`` binary to be installed and on PATH.
    """

    def __init__(
        self,
        image_handler: ImageHandler,
        audio_handler: AudioHandler,
        frame_interval_seconds: int = 5,
        max_frames: int = 6,
        ffmpeg_path: str = "ffmpeg",
    ):
        self.image_handler = image_handler
        self.audio_handler = audio_handler
        self.frame_interval_seconds = frame_interval_seconds
        self.max_frames = max_frames
        self.ffmpeg_path = ffmpeg_path

    def process(self, video_bytes: bytes, filename: str = "video.mp4") -> str:
        if not video_bytes:
            raise ValueError("No video data provided.")

        if shutil.which(self.ffmpeg_path) is None:
            raise RuntimeError(
                "ffmpeg is not installed or not on PATH. Install it to "
                "enable video processing, e.g. `apt install ffmpeg`."
            )

        with tempfile.TemporaryDirectory() as tmpdir:
            video_path = os.path.join(tmpdir, filename)

            with open(video_path, "wb") as handle:
                handle.write(video_bytes)

            frame_descriptions = self._extract_and_describe_frames(video_path, tmpdir)
            transcript = self._extract_and_transcribe_audio(video_path, tmpdir)

        sections = []

        if transcript:
            sections.append(f"Audio transcript:\n{transcript}")

        if frame_descriptions:
            joined = "\n".join(
                f"- [~{timestamp}s] {description}"
                for timestamp, description in frame_descriptions
            )
            sections.append(f"Visual frames sampled from the video:\n{joined}")

        if not sections:
            raise ValueError(
                "Could not extract any audio or visual content from the video."
            )

        return "\n\n".join(sections)

    def _extract_and_describe_frames(self, video_path: str, tmpdir: str):
        frame_pattern = os.path.join(tmpdir, "frame_%03d.jpg")

        subprocess.run(
            [
                self.ffmpeg_path,
                "-y",
                "-i",
                video_path,
                "-vf",
                f"fps=1/{self.frame_interval_seconds}",
                "-frames:v",
                str(self.max_frames),
                frame_pattern,
            ],
            check=True,
            capture_output=True,
        )

        descriptions = []

        frame_files = sorted(
            name for name in os.listdir(tmpdir) if name.startswith("frame_")
        )

        for index, frame_file in enumerate(frame_files):
            with open(os.path.join(tmpdir, frame_file), "rb") as handle:
                image_bytes = handle.read()

            description = self.image_handler.describe(
                image_bytes,
                mime_type="image/jpeg",
            )

            descriptions.append((index * self.frame_interval_seconds, description))

        return descriptions

    def _extract_and_transcribe_audio(self, video_path: str, tmpdir: str) -> str:
        audio_path = os.path.join(tmpdir, "audio.mp3")

        result = subprocess.run(
            [
                self.ffmpeg_path,
                "-y",
                "-i",
                video_path,
                "-vn",
                "-acodec",
                "libmp3lame",
                audio_path,
            ],
            capture_output=True,
        )

        if result.returncode != 0 or not os.path.exists(audio_path):
            # Video has no audio track (or ffmpeg couldn't extract one) --
            # that's fine, frame descriptions alone are still useful.
            return ""

        with open(audio_path, "rb") as handle:
            audio_bytes = handle.read()

        try:
            return self.audio_handler.transcribe(audio_bytes, filename="audio.mp3")
        except ValueError:
            return ""
