# hania.py

from crewai import Agent, Task, Crew, LLM

from dotenv import load_dotenv
import os
load_dotenv()
llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROOQ_API_KEY")

 )

game_designer=Agent(
    role="Game Designer",
    goal="desingn a game for child relateg to space and astronomy",
    backstory="design a game for kid related to space you are a game professtion and you are a senior developer ",
    llm=llm
)

game_designer_task=Task(
    description="design a game for kid related to space you are a game professtion and you are a senior developer",
    expected_output="bbuild a game related to space ,astronomy and glaxies",
    agent=game_designer
)
game_reviewer=Agent(
    role="Game Reviewer",
    goal="review the game and rate it out of 10",
    backstory="you are a product maneger and tell the developer",
    llm=llm
)
game_reviewer_task=Task(
    description="review the game and rate it out of 10",
    expected_output="rate the game out of 10",
    agent=game_reviewer
)
game_improver=Agent(
    role="team lead of game developer",
    goal="improve the game design so that we can improve the review and feedback",
    backstory="you are a team lead of developer so that you can improve the game design so that we can improve the review and feedback ",
    llm=llm  
)
game_improver_task=Task(
    description="improve the game design so that we can improve the review and feedback also improve the tech and sack if needed",
    expected_output="improve the game design so that we can improve the review and feedback",
    agent=game_improver
)
crew=Crew(
    agents=[game_designer,game_reviewer,game_improver],
    tasks=[game_designer_task,game_reviewer_task,game_improver_task],
    verbose=False
)
result=crew.kickoff()
print(result)
