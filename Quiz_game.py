#5: Quiz Game Master
from crewai import Agent,Task,LLM,Crew
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import os
load_dotenv()
llm=LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

print(50*"=")
print("WELCOME TO QUIZ GAME  ")
print(50*"=")

name=input("What is your name:")
topic=input("Pick Topic for quiz whic u want:")
Search_tool=SerperDevTool()

#for quiz question
Creator=Agent(
    role="Question Creator",
    goal="you create questions for quiz which is also a fun question",
    backstory="you are quiz question creator which thake quiz for increase the knowlagde",
    llm=llm,
    tools=[Search_tool]
)

Creator_task=Task(
    description=f"make the question related to the{topic}this topic",
    expected_output="make the the easy question of single line",
    agent=Creator
)

creator_crew = Crew(agents=[Creator],  tasks=[Creator_task])
result = creator_crew.kickoff()

print(f"\n--- QUIZ QUESTION ---")
print(result)
print("----------------------\n")


user_answer = input("Your answer: ")

# score the answer
Host = Agent(
    role="Quiz Host",
    goal="Evaluate the user's answer and provide a fun response with a score.",
    backstory="You are a  game show host. You compare user answers to the truth  answer celebrate correct answers wildly, and give gentle corrections for mistakes.",
    llm=llm,
    verbose=True
)



Host_task = Task(
    description=f"The question was: {result}. The user answered: {user_answer}. Is it correct?",
    expected_output="Check Answer of user and  score out of 10.",
    agent=Host
)


host_crew = Crew(agents=[Host], tasks=[Host_task])
final_result = host_crew.kickoff()

print(final_result)


