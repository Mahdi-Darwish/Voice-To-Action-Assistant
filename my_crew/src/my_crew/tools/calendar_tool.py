import os
import datetime
from typing import List, Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from zoneinfo import ZoneInfo
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from pydantic import BaseModel, Field, field_validator
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDENTIALS_PATH = os.path.join("credentials", "credentials.json")
DEFAULT_TIMEZONE = "Asia/Beirut"
TOKEN_PATH = os.path.join("credentials", "token.json")
def get_calendar_service():
    """
    Handles the OAuth2 flow for Google Calendar.
    First run: opens a browser window for you to log in and consent.
    Later runs: reuses the cached token.json (auto-refreshes when expired).
    """
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_PATH):
                raise FileNotFoundError(
                    f"Missing {CREDENTIALS_PATH}. Download OAuth client "
                    "credentials from Google Cloud Console (see README.md) "
                    "and place them there."
                )
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as token_file:
            token_file.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)

class ScheduleMeetingInput(BaseModel):
    summary: str = Field(..., description="Short title of the meeting")
    start_time: str = Field(
        ...,
        description="Meeting start time in ISO 8601 format, e.g. '2026-08-29T10:00:00'",
    )
    end_time: str = Field(
        ...,
        description="Meeting end time in ISO 8601 format, e.g. '2026-08-29T10:30:00'",
    )
    attendees: List[str] = Field(
        ..., description="List of attendee email addresses, e.g. ['a@x.com', 'b@x.com']"
    )
    description: str = Field(
        default="", description="Optional longer description / agenda for the meeting"
    )
    @field_validator("start_time", "end_time")
    @classmethod
    def valid_iso(cls, v):
        try:
            parsed = datetime.datetime.fromisoformat(v)
        except ValueError:
            raise ValueError(f"'{v}' is not a valid ISO 8601 datetime")
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=ZoneInfo(DEFAULT_TIMEZONE)).replace(tzinfo=None)
        return parsed.isoformat()
    
class ScheduleMeetingTool(BaseTool):
    name: str = "schedule_meeting"
    description: str = (
        "Schedules a Google Meet meeting on Google Calendar. Requires a summary/title, "
        "a start_time and end_time (ISO 8601), and a list of attendee emails. "
        "Automatically creates a Google Meet video call link, sets reminders 24 hours "
        "and 1 hour before the meeting, and emails the invite (including the Meet link) "
        "to every attendee and to the organizer. Returns the Meet link and event summary. "
        "Use this tool whenever the user asks to schedule, set up, or book a meeting/call."
    )
    args_schema: Type[BaseModel] = ScheduleMeetingInput
    def _run(
        self,
        summary: str,
        start_time: str,
        end_time: str,
        attendees: List[str],
        description: str = "",
    ) -> str:
        try:
            service = get_calendar_service()
            event_body = {
                "summary": summary,
                "description": description,
                "start": {"dateTime": start_time, "timeZone": DEFAULT_TIMEZONE},
                "end": {"dateTime": end_time, "timeZone": DEFAULT_TIMEZONE  },
                "attendees": [{"email": email} for email in attendees],
                "conferenceData": {
                    "createRequest": {
                        "requestId": f"meet-{datetime.datetime.now().timestamp()}",
                        "conferenceSolutionKey": {"type": "hangoutsMeet"},
                    }
                },
                "reminders": {
                    "useDefault": False,
                    "overrides": [
                        {"method": "email", "minutes": 24 * 60},  # 24 hours before
                        {"method": "popup", "minutes": 24 * 60},
                        {"method": "email", "minutes": 60},        # 1 hour before
                        {"method": "popup", "minutes": 60},
                    ],
                },
            }
            event = (
                service.events()
                .insert(
                    calendarId="primary",
                    body=event_body,
                    conferenceDataVersion=1,  # required to actually generate the Meet link
                    sendUpdates="all",         # emails organizer + all attendees
                )
                .execute()
            )
            meet_link = event.get("hangoutLink", "No Meet link generated")
            event_link = event.get("htmlLink", "")

            return (
                f"Meeting '{summary}' scheduled successfully.\n"
                f"Google Meet link: {meet_link}\n"
                f"Calendar event: {event_link}\n"
                f"Start: {start_time} ({DEFAULT_TIMEZONE}) | End: {end_time} ({DEFAULT_TIMEZONE})\n"
                f"Attendees invited: {', '.join(attendees)}\n"
                f"Reminders set for 24 hours and 1 hour before the meeting.\n"
                f"Invitations with the Meet link were emailed to all attendees and the organizer."
            )
        except Exception as e:
            return f"Failed to schedule meeting: {str(e)}"