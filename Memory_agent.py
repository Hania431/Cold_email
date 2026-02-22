from crewai import Agent, Task, Crew, LLM

from dotenv import load_dotenv
import os
load_dotenv()
llm= LLM(

    model="gemini/gemini-2.5-flash",

    api_key=os.getenv("GEMINI_API_KEY")

)


freind=Agent(
    role="A best friend",
    goal="be a great friend and remember everything about user",
    backstory="you are a friend which never forget anything",

    llm=llm

)

name=input("what is your name?")

food=input("what is you favorite food?")

hobby=input("what is your hobby?")

remember_task=Task(

    description=f''' Remember these fact about {name}:

    -favorite food: {food}

    -favorite hobby: {hobby}

    

    say hi and confirm you remember''',

    expected_output="Freindly greeting with user facts",

    agent=freind

)

crew=Crew(

    agents=[freind],

    tasks=[remember_task],


    memory= True,
    output_log_file="crewlog.txt",
    embedder={
        "provider":"sentence-transformer",
        "config":  {
                "model":"all_MiniLM-L6-v2"
        }
    }

)

result = crew.kickoff()

print(result)
