import datetime
import tempfile
import os
import streamlit as st
# from my_crew.crew import VoiceAssistantCrew
from my_crew.crew import VoiceAssistantCrew

st.set_page_config(page_title="Voice Assistant Tester", page_icon="🎙️", layout="centered")
st.title("🎙️ Voice Assistant - Test Console")
st.caption(
    "Test the schedule_meeting / send_email agent, either by voice or by typing "
    "a command directly."
)
mode = st.radio(
    "Input method",
    ["Type text (skip Whisper)", "Record from microphone", "Upload audio file"],
    horizontal=True,
)
transcribed_text = None

if mode == "Type text (skip Whisper)":
    transcribed_text = st.text_area(
        "Type the command as if you'd spoken it",
        placeholder="Schedule a meeting with james@company.com tomorrow at 10am for 30 minutes about the roadmap",
        height=100,
    )
elif mode == "Record from microphone":
    col1, col2 = st.columns(2)
    with col1:
        whisper_model_size = st.selectbox(
            "Whisper model",
            ["tiny.en", "base.en", "small.en", "small"],
            index=1,
            key="mic_model_size",
            help="'.en' models are English-only: faster AND more accurate than the multilingual versions for English speech.",
        )
    with col2:
        whisper_language = st.selectbox(
            "Language", ["English", "Auto-detect"], index=0, key="mic_language"
        )
    audio_value = st.audio_input("Click to record, click again to stop")

    if audio_value is not None:
        if st.button("Transcribe"):
            with st.spinner("Transcribing with Whisper..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                    tmp.write(audio_value.read())
                    tmp_path = tmp.name

                from my_crew.speech_to_text import transcribe_audio

                lang_code = "en" if whisper_language == "English" else None
                text = transcribe_audio(tmp_path, model_size=whisper_model_size, language=lang_code)
                os.remove(tmp_path)

                st.session_state["transcribed_text"] = text

    if "transcribed_text" in st.session_state:
        st.text_area(
            "Transcribed text (editable before sending)",
            key="transcribed_text",
            height=100,
        )
        transcribed_text = st.session_state["transcribed_text"]

else:
    whisper_model_size = st.selectbox(
        "Whisper model size", ["tiny", "base", "small", "medium"], index=1, key="upload_model_size"
    )
    audio_file = st.file_uploader(
        "Upload an audio file", type=["wav", "mp3", "m4a", "ogg", "webm"]
    )

    if audio_file is not None:
        st.audio(audio_file)

        if st.button("Transcribe"):
            with st.spinner("Transcribing with Whisper..."):
                suffix = os.path.splitext(audio_file.name)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(audio_file.read())
                    tmp_path = tmp.name
                from my_crew.speech_to_text import transcribe_audio
                text = transcribe_audio(tmp_path, model_size=whisper_model_size)
                os.remove(tmp_path)
                st.session_state["transcribed_text"] = text
    if "transcribed_text" in st.session_state:
        st.text_area(
            "Transcribed text (editable before sending)",
            key="transcribed_text",
            height=100,
        )
        transcribed_text = st.session_state["transcribed_text"]
st.divider()
run_disabled = not transcribed_text
if st.button("Run agent", type="primary", disabled=run_disabled):
    inputs = {
        "transcribed_text": transcribed_text,
        "current_datetime": datetime.datetime.now().isoformat(timespec="seconds"),
    }
    with st.spinner("Agent is thinking and picking a tool..."):
        try:
            result = VoiceAssistantCrew().crew().kickoff(inputs=inputs)
            st.success("Done")
            st.subheader("Result")
            st.markdown(str(result))
        except Exception as e:
            st.error(f"Something went wrong: {e}")
if run_disabled:
    st.info("Enter or transcribe some text above, then click Run agent.")