# Voice Assistant

A voice-driven assistant built with CrewAI that can understand a user's request and either schedule a Google Meet meeting or send an email.

The application supports both voice and text input. Voice commands are transcribed locally using OpenAI Whisper. If the transcription is inaccurate, the user can enter or edit the command manually before sending it to the agent.

## Features

- Voice-to-text using OpenAI Whisper
- Manual text input as a fallback for inaccurate transcriptions
- CrewAI agent for understanding requests and selecting the appropriate tool
- Gemini for agent reasoning
- Google Calendar integration
- Automatic Google Meet link generation
- Meeting reminders and attendee invitations
- Gmail SMTP integration for sending emails
- Streamlit interface for voice, text, and audio-file inputs

## Project Structure

```text
voice_assistant_project/
├── .vscode/
├── credentials/
│   ├── credentials.json
│   └── token.json
├── my_crew/
│   ├── pyproject.toml
│   └── src/
│       └── my_crew/
│           ├── crew.py
│           ├── main.py
│           ├── speech_to_text.py
│           ├── config/
│           │   ├── agents.yaml
│           │   └── tasks.yaml
│           └── tools/
│               ├── calendar_tool.py
│               └── email_tool.py
├── .gitignore
├── app.py
├── README.md
└── requirements.txt
```

`venv/` and `.env` are local files and should not be committed to the repository.

## Technologies

- Python
- CrewAI
- Gemini
- OpenAI Whisper
- Google Calendar API
- Gmail SMTP
- Streamlit

## Setup

### 1. Install FFmpeg

Whisper requires FFmpeg to process audio files.

**macOS:**

```bash
brew install ffmpeg
```

**Ubuntu/Debian:**

```bash
sudo apt install ffmpeg
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Install the CrewAI project:

```bash
cd my_crew
pip install -e .
cd ..
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GMAIL_ADDRESS=youraddress@gmail.com
GMAIL_APP_PASSWORD=your_app_password
GEMINI_API_KEY=your_gemini_api_key
```

### 5. Configure Google Calendar

Create a Google Cloud project and enable the Google Calendar API.

Create a Desktop OAuth client and place the downloaded credentials file at:

```text
credentials/credentials.json
```

The application will generate `token.json` after the first Google authentication.

## Running the Application

Start the Streamlit interface:

```bash
python -m streamlit run app.py
```

The interface supports:

- Text input
- Microphone input
- Audio file upload

If Whisper produces an incorrect transcription, the command can be manually entered or corrected before running the agent.

## Example Commands

### Schedule a meeting

```text
Schedule a meeting with james@company.com tomorrow at 10am
for 30 minutes about the project roadmap.
```

The agent selects the `schedule_meeting` tool, creates the Google Calendar event, generates a Google Meet link, and adds the attendees and reminders.

### Send an email

```text
Send an email to james@company.com saying I'll be two hours late.
```

The agent selects the `send_email` tool and sends the message through Gmail SMTP.

## Security

Do not commit credentials or secrets to GitHub.

Add the following to `.gitignore`:

```gitignore
.env
venv/
credentials/token.json
credentials/credentials.json
__pycache__/
*.pyc
```

If a credential is accidentally committed, revoke or regenerate it immediately.

## License

MIT