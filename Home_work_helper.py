import streamlit as st
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="Homework Helper",
    page_icon="📚",
    layout="centered"
)

st.title("📚 Homework Helper")
st.markdown("Get help with your homework questions using AI-powered research and explanations!")

if "result" not in st.session_state:
    st.session_state.result = None
if "loading" not in st.session_state:
    st.session_state.loading = False

with st.form("homework_form"):
    name = st.text_input("What's your name?", placeholder="Enter your name")
    subject = st.selectbox(
        "What subject?",
        ["Math", "Science", "History", "English", "Geography", "Physics", "Chemistry", "Biology", "Other"]
    )
    question = st.text_area("What's your homework question?", placeholder="Type your question here...")
    submitted = st.form_submit_button("Get Help!", use_container_width=True)

def get_homework_help(name, subject, question):
    llm = LLM(
        model="gemini/gemini-2.5-flash",
        api_key=os.getenv("GEMINI_API_KEY")
    )
    
    search_tool = SerperDevTool()
    
    researcher = Agent(
        role="Homework Researcher",
        goal="Find accurate and comprehensive information for homework questions",
        backstory="You are an expert researcher who helps students find reliable information for their homework. You search for facts, data, and explanations from credible sources.",
        llm=llm,
        tools=[search_tool],
        verbose=True
    )
    
    teacher = Agent(
        role="Friendly Teacher",
        goal="Explain concepts in a simple, engaging way that students can understand",
        backstory="You are a patient and enthusiastic teacher who makes learning fun and easy. You break down complex topics into simple explanations suitable for students.",
        llm=llm,
        tools=[search_tool],
        verbose=True
    )
    
    researcher_task = Task(
        description=f"Research this {subject} question thoroughly: {question}. Find accurate facts, data, and information from reliable sources.",
        expected_output="Detailed research findings with facts and information about the question",
        agent=researcher
    )
    
    teacher_task = Task(
        description=f"Based on the research, explain the answer to '{question}' to {name} in a simple, kid-friendly way. Make it engaging and easy to understand.",
        expected_output="A clear, friendly explanation suitable for a student",
        agent=teacher
    )
    
    crew = Crew(
        agents=[researcher, teacher],
        tasks=[researcher_task, teacher_task],
        verbose=False
    )
    
    result = crew.kickoff()
    return result

if submitted:
    if not name or not question:
        st.error("Please fill in your name and question!")
    else:
        st.session_state.loading = True
        with st.spinner("🔍 Researching your question... This may take a moment."):
            try:
                result = get_homework_help(name, subject, question)
                st.session_state.result = result
                st.session_state.loading = False
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.session_state.loading = False

if st.session_state.result:
    st.success("Here's your homework help!")
    st.markdown("---")
    st.markdown("### Answer")
    st.write(st.session_state.result)
    
    if st.button("Ask Another Question"):
        st.session_state.result = None
        st.rerun()

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Powered by Gemini 2.5 Flash & CrewAI</p>", unsafe_allow_html=True)
