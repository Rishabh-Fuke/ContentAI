from crewai import Agent, Crew, Process, Task #type:ignore
from crewai.project import CrewBase, agent, crew, task #type:ignore
from crewai.agents.agent_builder.base_agent import BaseAgent #type:ignore
# built-in and custom tools
from crewai_tools import SerperDevTool #type:ignore
from autogram.tools.collector_tool import CollectorTool
from autogram.tools.summarizer_tool import SummarizerTool
from autogram.tools.formatter_tool import FormatterTool
from autogram.tools.veo_tool import VeoTool
import os

# from crewai_tools import ScrapeWebsiteTool  # Commented out for now
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

# Tool registration map for CrewAI
tool_functions = {
    "veo_tool": VeoTool,
    "collector_tool": CollectorTool,
    "summarizer_tool": SummarizerTool,
    "formatter_tool": FormatterTool,
    # add others if needed
}


@CrewBase
class Autogram():
    """Autogram crew"""

    agents: List[BaseAgent]
    tasks: List[Task]


 
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], 
            tools=[SerperDevTool(), CollectorTool()], 
            verbose=True
        )
    

    @agent
    def summarizer(self) -> Agent:
        """Summarizer agent: consumes research output and produces concise summaries using summarizer tool."""
        return Agent(
            config=self.agents_config['summarizer'], 
            tools=[SummarizerTool()],
            verbose=True
        )

    @agent
    def content_creator(self) -> Agent:
        """Content Creator agent: takes the summary from the summarizer agent and creates a full script for the instagram video"""
        return Agent(
            config=self.agents_config['content_creator'], 
            tools=[FormatterTool()],
            verbose=True
        )
    
    @agent
    def video_generator(self) -> Agent:
        """Generates a video using Google Veo 3 from the script produced by the content_creator."""
        veo_api_key = os.getenv("GOOGLE_VEO_API_KEY", "")
        if not veo_api_key:
            raise ValueError("GOOGLE_VEO_API_KEY not found in environment variables.")
        
        return Agent(
            config=self.agents_config['video_generator'],
            tools=[VeoTool(api_key=veo_api_key)],
            verbose=True,
            instructions="Use the VeoTool to generate a video using the script text from the 'report.md' file.",
            
        )


  

    
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], 
        )

    @task
    def summarize_task(self) -> Task:
        return Task(
            config=self.tasks_config['summarize_task'],
                )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'], 
            output_file='report.md' #Saves the final script to report.md for ease of viewing. Could pass the file to another agent for video generation
        )
    
    @task
    def video_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['video_generation_task'],
            inputs={
            "script_file": "report.md" 
            },
            output_file='autogram_output.mp4'
        )


    @crew
    def crew(self) -> Crew:
        """Creates the Autogram crew"""
       

        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
            tools=tool_functions,
       
        )
