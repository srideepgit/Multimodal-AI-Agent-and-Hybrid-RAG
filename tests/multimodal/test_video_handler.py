import os
from unittest.mock import MagicMock, patch

import pytest

from app.multimodal.video_handler import VideoHandler


def _make_handler():
    image_handler = MagicMock()
    image_handler.describe.return_value = "A slide showing quarterly revenue."

    audio_handler = MagicMock()
    audio_handler.transcribe.return_value = "In this video we cover Q3 results."

    handler = VideoHandler(
        image_handler=image_handler,
        audio_handler=audio_handler,
        frame_interval_seconds=5,
        max_frames=2,
        ffmpeg_path="ffmpeg",
    )

    return handler, image_handler, audio_handler


def _fake_ffmpeg_run(tmpdir_holder):
    """
    Stand-in for subprocess.run that "extracts" frames/audio by writing
    placeholder files into the temp dir ffmpeg would have written to.
    """

    def _run(cmd, **kwargs):
        tmpdir = tmpdir_holder["path"]

        if "-vf" in cmd:
            # Frame extraction call.
            for i in range(1, 3):
                with open(os.path.join(tmpdir, f"frame_{i:03d}.jpg"), "wb") as f:
                    f.write(b"fake-jpeg-bytes")
        elif "-acodec" in cmd:
            # Audio extraction call.
            with open(os.path.join(tmpdir, "audio.mp3"), "wb") as f:
                f.write(b"fake-mp3-bytes")

        result = MagicMock()
        result.returncode = 0
        return result

    return _run


def test_process_combines_frames_and_transcript():
    handler, image_handler, audio_handler = _make_handler()
    tmpdir_holder = {}

    original_temp_dir = __import__("tempfile").TemporaryDirectory

    class TrackingTempDir:
        def __enter__(self_inner):
            self_inner._ctx = original_temp_dir()
            path = self_inner._ctx.__enter__()
            tmpdir_holder["path"] = path
            return path

        def __exit__(self_inner, *args):
            return self_inner._ctx.__exit__(*args)

    with patch("app.multimodal.video_handler.shutil.which", return_value="/usr/bin/ffmpeg"), \
         patch("app.multimodal.video_handler.tempfile.TemporaryDirectory", TrackingTempDir), \
         patch("app.multimodal.video_handler.subprocess.run", side_effect=_fake_ffmpeg_run(tmpdir_holder)):

        result = handler.process(b"fake-video-bytes", filename="clip.mp4")

    assert "Audio transcript" in result
    assert "In this video we cover Q3 results." in result
    assert "Visual frames" in result
    assert "A slide showing quarterly revenue." in result
    assert image_handler.describe.call_count == 2
    audio_handler.transcribe.assert_called_once()


def test_process_rejects_empty_input():
    handler, _, _ = _make_handler()

    with pytest.raises(ValueError):
        handler.process(b"")


def test_process_requires_ffmpeg():
    handler, _, _ = _make_handler()

    with patch("app.multimodal.video_handler.shutil.which", return_value=None):
        with pytest.raises(RuntimeError):
            handler.process(b"fake-video-bytes")
