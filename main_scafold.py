import sys
import datetime
from my_crew.speech_to_text import transcribe_audio
from my_crew.src.my_crew.crew import VoiceAssistantCrew

def run_pipeline(audio_file_path: str, whisper_model_size: str = "base"):
    print(f"[1/2] Transcribing '{audio_file_path}' with Whisper ({whisper_model_size})...")
    transcribed_text = transcribe_audio(audio_file_path, model_size=whisper_model_size)
    print(f"      -> Transcribed text: {transcribed_text!r}")
    print("[2/2] Running the crew...\n")
    inputs = {
        "transcribed_text": transcribed_text,
        "current_datetime": datetime.datetime.now().isoformat(timespec="seconds"),
    }
    result = VoiceAssistantCrew().crew().kickoff(inputs=inputs)
    print("\n=== FINAL RESULT ===")
    print(result)
    return result
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_audio_file> [whisper_model_size]")
        sys.exit(1)
    audio_path = sys.argv[1]
    model_size = sys.argv[2] if len(sys.argv) > 2 else "base"
    run_pipeline(audio_path, model_size)