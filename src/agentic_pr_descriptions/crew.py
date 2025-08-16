from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class PRDescriptionCrew:
    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def pr_description_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["pr_description_agent"],
        )

    @task
    def generate_pr_description_task(self) -> Task:
        return Task(
            config=self.tasks_config["generate_pr_description_task"],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
