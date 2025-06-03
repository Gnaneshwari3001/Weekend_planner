import yaml
import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from crewai_tools.tools.website_search.website_search_tool import WebsiteSearchTool
from dotenv import load_dotenv

load_dotenv()

@CrewBase
class WeekendPlannerCrew:
    """WeekendPlannerCrew crew"""

    def __init__(self):
        # This gets the directory of the current file (crew.py)
        # For example: F:\Weekend_Planner\weekend_planner_crew
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        
        # This constructs the path to the config folder:
        # F:\Weekend_Planner\weekend_planner_crew\config
        config_dir = os.path.join(current_file_dir, "config")

        # This constructs the full path to the YAML files:
        # F:\Weekend_Planner\weekend_planner_crew\config\agents.yaml
        agents_config_path = os.path.join(config_dir, "agents.yaml")
        # F:\Weekend_Planner\weekend_planner_crew\config\tasks.yaml
        tasks_config_path = os.path.join(config_dir, "tasks.yaml")

        print(f"DEBUG: Attempting to load agents config from: {agents_config_path}")
        print(f"DEBUG: Attempting to load tasks config from: {tasks_config_path}")

        try:
            with open(agents_config_path, 'r', encoding='utf-8') as f:
                raw_agents_content = f.read()
                print(f"DEBUG: Raw agents.yaml content read (first 100 chars): '{raw_agents_content[:100]}'")
                f.seek(0) # Reset file pointer to the beginning for yaml.safe_load
                self.agents_config = yaml.safe_load(f)
            print(f"DEBUG: Loaded agents_config: {self.agents_config is not None} (Type: {type(self.agents_config)})")

            with open(tasks_config_path, 'r', encoding='utf-8') as f:
                raw_tasks_content = f.read()
                print(f"DEBUG: Raw tasks.yaml content read (first 100 chars): '{raw_tasks_content[:100]}'")
                f.seek(0) # Reset file pointer to the beginning for yaml.safe_load
                self.tasks_config = yaml.safe_load(f)
            print(f"DEBUG: Loaded tasks_config: {self.tasks_config is not None} (Type: {type(self.tasks_config)})")

        except FileNotFoundError as e:
            print(f"ERROR: Config file not found: {e}. Please check path and file existence.")
            self.agents_config = {} # Default to empty dict to prevent NoneType errors later
            self.tasks_config = {}
        except yaml.YAMLError as e:
            print(f"ERROR: Error parsing YAML config: {e}. Please check YAML syntax.")
            self.agents_config = {}
            self.tasks_config = {}

    @agent
    def weekend_itinerary_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["weekend_itinerary_agent"],
            verbose=True,
            tools=[SerperDevTool(), WebsiteSearchTool()],
        )

    @agent
    def activity_curator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["activity_curator_agent"],
            verbose=True,
            tools=[SerperDevTool(), WebsiteSearchTool()],
        )

    @agent
    def dining_expert_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["dining_expert_agent"],
            verbose=True,
            tools=[SerperDevTool(), WebsiteSearchTool()],
        )

    @agent
    def local_insights_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["local_insights_agent"],
            verbose=True,
            tools=[SerperDevTool(), WebsiteSearchTool()],
        )

    @agent
    def weather_monitor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["weather_monitor_agent"],
            verbose=True,
            tools=[SerperDevTool(), WebsiteSearchTool()],
        )

    @agent
    def transport_navigator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["transport_navigator_agent"],
            verbose=True,
            tools=[SerperDevTool(), WebsiteSearchTool()],
        )

    @agent
    def budget_advisor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["budget_advisor_agent"],
            verbose=True,
            tools=[SerperDevTool(), WebsiteSearchTool()],
        )

    @task
    def itinerary_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config["itinerary_creation_task"],
            output_file="output/weekend_itinerary.md",
        )

    @task
    def activity_discovery_task(self) -> Task:
        return Task(
            config=self.tasks_config["activity_discovery_task"],
            output_file="output/weekend_activities.md",
        )

    @task
    def dining_suggestions_task(self) -> Task:
        return Task(
            config=self.tasks_config["dining_suggestions_task"],
            output_file="output/weekend_dining.md",
        )

    @task
    def local_guidance_task(self) -> Task:
        return Task(
            config=self.tasks_config["local_guidance_task"],
            output_file="output/local_guidance.md",
        )

    @task
    def weather_check_task(self) -> Task:
        return Task(
            config=self.tasks_config["weather_check_task"],
            output_file="output/weekend_weather.md",
        )

    @task
    def transport_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config["transport_planning_task"],
            output_file="output/weekend_transport.md",
        )

    @task
    def budget_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config["budget_analysis_task"],
            output_file="output/weekend_budget.md",
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )