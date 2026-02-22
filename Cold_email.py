import os
import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import ScrapeWebsiteTool
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# ─── LLM Setup ────────────────────────────────────────────────────────────────
# Option 1: Gemini (Google)
llm = LLM(
      model="gemini/gemini-2.5-flash",
     api_key=os.getenv("GEMINI_API_KEY")
 )

# Option 2: OpenAI
# llm = LLM(
#     model="gpt-4o-mini",
#     api_key=os.getenv("OPENAI_API_KEY")
# )



agency_services = """
1. SEO Optimization Service: Best for companies with good products but low traffic. We increase organic reach.
2. Custom Web Development: Best for companies with outdated, ugly, or slow websites. We build modern React/Python sites.
3. AI Automation: Best for companies with manual, repetitive tasks. We build agents to save time.
"""

scrape_tool = ScrapeWebsiteTool()

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Cold Email Agent",
    page_icon="📧",
    layout="centered"
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&display=swap');

* { font-family: 'Sora', sans-serif; }

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0a0f, #111827, #0f172a);
    color: #e2e8f0;
}
[data-testid="stHeader"] { background: transparent; }

.hero-title {
    font-size: 2.6rem;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.3rem;
}
.hero-sub {
    text-align: center;
    color: #64748b;
    font-size: 0.95rem;
    margin-bottom: 2rem;
}
.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(56,189,248,0.15);
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(10px);
}
.result-box {
    background: rgba(52,211,153,0.05);
    border: 1px solid rgba(52,211,153,0.2);
    border-radius: 16px;
    padding: 1.8rem;
    margin-top: 1.5rem;
}
.analysis-box {
    background: rgba(129,140,248,0.05);
    border: 1px solid rgba(129,140,248,0.2);
    border-radius: 16px;
    padding: 1.5rem;
    margin-top: 1rem;
}
.strategy-box {
    background: rgba(251,146,60,0.05);
    border: 1px solid rgba(251,146,60,0.2);
    border-radius: 16px;
    padding: 1.5rem;
    margin-top: 1rem;
}
.step-badge {
    display: inline-block;
    background: rgba(129,140,248,0.15);
    border: 1px solid rgba(129,140,248,0.3);
    border-radius: 20px;
    padding: 0.15rem 0.75rem;
    font-size: 0.75rem;
    color: #818cf8;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}
.label {
    font-size: 0.85rem;
    font-weight: 600;
    color: #7dd3fc;
    margin-bottom: 0.4rem;
}
.stButton > button {
    background: linear-gradient(135deg, #0ea5e9, #6366f1);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.7rem 2rem;
    font-size: 1rem;
    font-weight: 600;
    width: 100%;
    box-shadow: 0 4px 20px rgba(14,165,233,0.35);
    transition: all 0.3s ease;
}
.stButton > button:hover {
    box-shadow: 0 6px 28px rgba(14,165,233,0.55);
    transform: translateY(-1px);
}
.stButton > button:disabled {
    background: linear-gradient(135deg, #334155, #475569);
    box-shadow: none;
    cursor: not-allowed;
}
.footer {
    text-align: center;
    color: #334155;
    font-size: 0.78rem;
    margin-top: 3rem;
    padding-bottom: 2rem;
}
.history-item {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(56,189,248,0.1);
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 0.8rem;
}
</style>
""", unsafe_allow_html=True)

# ─── Session State ────────────────────────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None
if "analysis" not in st.session_state:
    st.session_state.analysis = None
if "strategy" not in st.session_state:
    st.session_state.strategy = None
if "history" not in st.session_state:
    st.session_state.history = []
if "is_generating" not in st.session_state:
    st.session_state.is_generating = False
if "target_url" not in st.session_state:
    st.session_state.target_url = ""
if "ceo_name" not in st.session_state:
    st.session_state.ceo_name = ""
if "sender_name" not in st.session_state:
    st.session_state.sender_name = ""

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">📧 Cold Email Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Enter any company URL — get a personalized cold email in seconds</div>', unsafe_allow_html=True)

# ─── Input Card ───────────────────────────────────────────────────────────────
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="step-badge">✦ Target Input</div>', unsafe_allow_html=True)

st.markdown('<p class="label">🌐 Company Website URL</p>', unsafe_allow_html=True)
target_url = st.text_input(
    "url_input",
    value=st.session_state.target_url,
    placeholder="https://example.com",
    label_visibility="collapsed"
)

st.markdown('<p class="label">👤 CEO / Contact Name (optional)</p>', unsafe_allow_html=True)
ceo_name = st.text_input(
    "ceo_input",
    value=st.session_state.ceo_name,
    placeholder="e.g. John Smith (leave blank to auto-detect)",
    label_visibility="collapsed"
)

st.markdown('<p class="label">🎯 Your Name (for email signature)</p>', unsafe_allow_html=True)
sender_name = st.text_input(
    "sender_input",
    value=st.session_state.sender_name,
    placeholder="e.g. Alex from Growth Agency",
    label_visibility="collapsed"
)

st.markdown('</div>', unsafe_allow_html=True)

# ─── CrewAI Runner ────────────────────────────────────────────────────────────
def run_crew(target_url, ceo_name, sender_name):
    researcher = Agent(
        role="Business Intelligence Analyst",
        goal="Analyze the target company website and identify their core business and potential weaknesses.",
        backstory="You are an expert at analyzing businesses just by looking at their landing page. You look for what they do and where they might be struggling.",
        tools=[scrape_tool],
        verbose=True,
        allow_delegation=False,
        memory=True,
        llm=llm
    )

    strategist = Agent(
        role="Agency Strategist",
        goal="Match the target company needs with ONE of our agency services.",
        backstory=f"""You work for a top-tier digital agency.
        Your goal is to read the analysis of a prospect and decide which of OUR services to pitch.

        OUR SERVICES KNOWLEDGE BASE:
        {agency_services}

        You must pick the SINGLE best service for this specific client and explain why.""",
        verbose=True,
        memory=True,
        llm=llm
    )

    writer = Agent(
        role="Senior Sales Copywriter",
        goal="Write a personalized cold email that sounds human and professional.",
        backstory="""You write emails that get replies. You never sound robotic.
        You mention specific details found by the Researcher to prove we actually looked at their site.""",
        verbose=True,
        memory=True,
        llm=llm
    )

    task_analyze = Task(
        description=f"Scrape the website {target_url}. Summarize what the company does and identify 1 key area where they could improve (e.g., design, traffic, automation).",
        expected_output="A brief summary of the company and their potential pain points.",
        agent=researcher
    )

    task_strategize = Task(
        description="Based on the analysis, pick ONE service from our Agency Knowledge Base that solves their problem. Explain the match.",
        expected_output="The selected service and the reasoning for the match.",
        agent=strategist,
        context=[task_analyze]
    )

    task_write = Task(
        description=f"Draft a cold email to the CEO of the target company. Pitch the selected service. Keep it under 150 words. Sign as: {sender_name if sender_name else 'Best regards'}",
        expected_output="A professional cold email ready to send.",
        agent=writer,
        context=[task_analyze, task_strategize]
    )

    sales_crew = Crew(
        agents=[researcher, strategist, writer],
        tasks=[task_analyze, task_strategize, task_write],
        process=Process.sequential,
        verbose=True
    )

    result = sales_crew.kickoff()
    
    analysis_output = task_analyze.output.raw if task_analyze.output else "Analysis not available"
    strategy_output = task_strategize.output.raw if task_strategize.output else "Strategy not available"
    
    return result, analysis_output, strategy_output

# ─── Generate Button ──────────────────────────────────────────────────────────
run_button = st.button(
    "🚀 Generate Cold Email",
    disabled=st.session_state.is_generating or not target_url,
    use_container_width=True
)

# ─── Processing ───────────────────────────────────────────────────────────────
if run_button and target_url:
    st.session_state.target_url = target_url
    st.session_state.ceo_name = ceo_name
    st.session_state.sender_name = sender_name
    st.session_state.is_generating = True
    st.session_state.result = None
    st.session_state.analysis = None
    st.session_state.strategy = None
    st.rerun()

if st.session_state.is_generating and st.session_state.target_url:
    with st.status("🤖 AI Agents at work...", expanded=True) as status:
        st.write("🔍 Researcher: Analyzing company website...")
        
        try:
            result, analysis, strategy = run_crew(
                st.session_state.target_url, 
                st.session_state.ceo_name, 
                st.session_state.sender_name
            )
            
            st.session_state.result = result
            st.session_state.analysis = analysis
            st.session_state.strategy = strategy
            st.session_state.is_generating = False
            
            st.session_state.history.append({
                'url': st.session_state.target_url,
                'email': str(result),
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            
            status.update(label="✅ Email generated successfully!", state="complete")
            st.rerun()
            
        except Exception as e:
            st.session_state.is_generating = False
            status.update(label=f"❌ Error: {str(e)}", state="error")
            st.error(f"An error occurred: {str(e)}")

# ─── Results Display ──────────────────────────────────────────────────────────
if st.session_state.analysis:
    with st.expander("🔍 Company Analysis", expanded=False):
        st.markdown('<div class="analysis-box">', unsafe_allow_html=True)
        st.markdown(st.session_state.analysis)
        st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.strategy:
    with st.expander("📋 Strategy", expanded=False):
        st.markdown('<div class="strategy-box">', unsafe_allow_html=True)
        st.markdown(st.session_state.strategy)
        st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.result:
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.markdown('<div class="step-badge">✦ Generated Email</div>', unsafe_allow_html=True)
    
    email_text = str(st.session_state.result)
    st.text_area("Email Content", email_text, height=300, label_visibility="collapsed")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ─── History Section ──────────────────────────────────────────────────────────
if st.session_state.history:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="step-badge">✦ History</div>', unsafe_allow_html=True)
    
    for i, item in enumerate(reversed(st.session_state.history[-5:])):
        st.markdown(f'<div class="history-item">', unsafe_allow_html=True)
        st.write(f"**{item['url']}** - {item['timestamp']}")
        with st.expander("View Email"):
            st.text(item['email'][:500] + "..." if len(item['email']) > 500 else item['email'])
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown('<div class="footer">Powered by CrewAI + Streamlit</div>', unsafe_allow_html=True)
