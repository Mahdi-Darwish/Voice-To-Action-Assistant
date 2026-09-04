# 🎙️ Voice Assistant — CrewAI + Whisper

A voice-driven AI assistant that understands natural-language commands and uses a CrewAI agent to either **schedule a Google Meet meeting** or **send an email**.

```text
🎙️ Voice
   ↓
🧠 Whisper — Speech to Text
   ↓
🤖 CrewAI + Gemini
   ↓
 ┌──────────────────┬─────────────────┐
 📅 Schedule Meeting   📧 Send Email
        ↓                    ↓
 Google Calendar         Gmail SMTP
 + Google Meet
```

## ✨ Features

* 🎙️ Local speech-to-text with **OpenAI Whisper**
* 🤖 AI agent using **CrewAI + Gemini**
* 📅 Creates Google Calendar events with Google Meet links
* ⏰ Adds meeting reminders and attendee invitations
* 📧 Sends emails through Gmail SMTP
* 🖥️ Streamlit interface for text, microphone, and audio-file input
* 🔐 API keys and credentials stored in `.env`

## 🛠️ Tech Stack

| Component      | Technology          |
| -------------- | ------------------- |
| Speech-to-text | OpenAI Whisper      |
| Agent          | CrewAI `0.114.0`    |
| LLM            | Gemini              |
| Calendar       | Google Calendar API |
| Email          | Gmail SMTP          |
| UI             | Streamlit           |

## 📁 Project Structure

```text
voice_assistant_project/
├── app.py
├── requirements.txt
├── .env
├── credentials/
│   ├── credentials.json
│   └── token.json
└── my_crew/
    └── src/my_crew/
        ├── crew.py
        ├── main.py
        ├── speech_to_text.py
        ├── config/
        │   ├── agents.yaml
        │   └── tasks.yaml
        └── tools/
            ├── calendar_tool.py
            └── email_tool.py
```

## 🚀 Setup

### 1. Install FFmpeg

**macOS:**

```bash
brew install ffmpeg
```

**Ubuntu/Debian:**

```bash
sudo apt install ffmpeg
```

### 2. Clone and install

```bash
git clone <your-repo-url>
cd voice_assistant_project

python -m venv venv
source venv/bin/activate

cd my_crew
pip install -e .
cd ..

pip install -r requirements.txt
```

### 3. Configure credentials

Create a `.env` file:

```env
GMAIL_ADDRESS=youraddress@gmail.com
GMAIL_APP_PASSWORD=your_app_password
GEMINI_API_KEY=your_gemini_api_key
```

For Google Calendar, create OAuth credentials in Google Cloud Console and place them at:

```text
credentials/credentials.json
```

The application will generate `token.json` after the first Google login.

## ▶️ Run

Start the Streamlit interface:

```bash
python -m streamlit run app.py
```

Or run from an audio file:

```bash
cd my_crew/src/my_crew
python main.py path/to/audio.wav
```

## 💬 Example

```text
"Schedule a meeting with james@company.com tomorrow at 10am
for 30 minutes about the roadmap."
```

→ Creates a Google Calendar event with a Google Meet link.

```text
"Send an email to james@company.com saying I'll be 2 hours late."
```

→ Sends the email through Gmail SMTP.

## 🔒 Security

Never commit secrets to GitHub:

```gitignore
.env
venv/
credentials/token.json
credentials/credentials.json
__pycache__/
```

## 📄 License

MIT
