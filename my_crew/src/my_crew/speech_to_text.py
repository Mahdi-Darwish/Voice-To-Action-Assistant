"""
Speech-to-text using OpenAI's open-source Whisper model.
Runs 100% locally -> free, no API key needed.

Requires the `ffmpeg` system binary to be installed:
  - Ubuntu/Debian: sudo apt install ffmpeg
  - Mac (brew):    brew install ffmpeg
  - Windows:       choco install ffmpeg  (or download from ffmpeg.org)
"""

import whisper

# Cache the model so we don't reload it on every call.
_model_cache = {}


def _get_model(model_size: str = "base"):
    """
    Whisper model sizes (speed vs accuracy tradeoff), all free:
      tiny   -> fastest, least accurate
      base   -> good default for short commands
      small  -> better accuracy, still fast on CPU
      medium -> much better accuracy, needs more RAM/CPU or a GPU
      large  -> best accuracy, slow on CPU
    """
    if model_size not in _model_cache:
        _model_cache[model_size] = whisper.load_model(model_size)
    return _model_cache[model_size]


# A default prompt that primes Whisper toward the vocabulary/format this
# app actually expects. Whisper conditions on this text, which measurably
# improves accuracy on email addresses, names, and relative times -
# the things it gets wrong most often otherwise.
DEFAULT_PROMPT = (
    "Voice command for scheduling meetings or sending emails. "
    "May include an email address like james@company.com or "
    "mahdidarwish2024@gmail.com, spoken with 'at' and 'dot'. "
    "May include a relative time like 'tomorrow at 3pm' or 'in 2 hours'. "
    "May include phrases like 'schedule a meeting with', "
    "'send an email to', or 'tell him that'."
)


def transcribe_audio(
    audio_path: str,
    model_size: str = "base",
    language: str = None,
    initial_prompt: str = DEFAULT_PROMPT,
) -> str:
    """
    Transcribe an audio file (wav, mp3, m4a, etc.) into text.

    Args:
        audio_path: path to the audio file
        model_size: which whisper model to load (see _get_model docstring)
        language: optional ISO language code (e.g. "en") to skip
                   language auto-detection and speed things up.
        initial_prompt: text Whisper conditions on before transcribing,
                   used to bias it toward expected vocabulary/format.
                   Pass None to disable.

    Returns:
        The transcribed text as a string.
    """
    model = _get_model(model_size)
    result = model.transcribe(audio_path, language=language, initial_prompt=initial_prompt)
    return result["text"].strip()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python speech_to_text.py <path_to_audio_file>")
        sys.exit(1)

    text = transcribe_audio(sys.argv[1])
    print("Transcription:")
    print(text)