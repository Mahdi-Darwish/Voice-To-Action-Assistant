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
def transcribe_audio(audio_path: str, model_size: str = "base", language: str = None) -> str:
    """
    Transcribe an audio file (wav, mp3, m4a, etc.) into text.

    Args:
        audio_path: path to the audio file
        model_size: which whisper model to load (see _get_model docstring)
        language: optional ISO language code (e.g. "en") to skip
                   language auto-detection and speed things up.

    Returns:
        The transcribed text as a string.
    """
    model = _get_model(model_size)
    result = model.transcribe(audio_path, language=language)
    return result["text"].strip()
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python speech_to_text.py <path_to_audio_file>")
        sys.exit(1)
    text = transcribe_audio(sys.argv[1])
    print("Transcription:")
    print(text)