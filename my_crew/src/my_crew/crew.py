import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
from my_crew.tools.calendar_tool import ScheduleMeetingTool
from my_crew.tools.email_tool import SendEmailTool

load_dotenv()
llm = LLM(
    model="gemini/gemini-3.1-flash-lite",
    api_key=os.getenv("GEMINI_API_KEY"),
)
@CrewBase
class VoiceAssistantCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    @agent
    def voice_command_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["voice_command_agent"],
            tools=[ScheduleMeetingTool(), SendEmailTool()],
            llm=llm,
            verbose=True,
        )
    @task
    def voice_command_task(self) -> Task:
        return Task(
            config=self.tasks_config["voice_command_task"],
            agent=self.voice_command_agent(),
        )
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )