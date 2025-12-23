"""
ERP Trend Agent - Multi-Agent System with Streamlit UI
A clean, modern dashboard for analyzing ERP industry trends using AutoGen agents.
"""

import streamlit as st
import asyncio
import plotly.graph_objects as go
from datetime import datetime
import re
import os
from dotenv import load_dotenv

# Import agent functions
from agents import create_agent_team, get_agent_info

load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="ERP Trend Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean, Modern CSS - Easy on the eyes
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    /* Clean Light Theme */
    .stApp {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main Header */
    .main-header {
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
        color: #1e293b;
        font-size: 2.5rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    .sub-header {
        text-align: center;
        color: #64748b;
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    /* Cards */
    .card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 4px 12px rgba(0,0,0,0.04);
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    
    .card-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 1rem;
    }
    
    /* Agent Pipeline Cards */
    .agent-step {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 16px;
        margin: 8px 0;
        background: #f8fafc;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        transition: all 0.2s ease;
    }
    
    .agent-step:hover {
        background: #f1f5f9;
        border-color: #cbd5e1;
    }
    
    .agent-step.active {
        background: linear-gradient(135deg, #dbeafe 0%, #e0e7ff 100%);
        border-color: #3b82f6;
    }
    
    .agent-step.completed {
        background: linear-gradient(135deg, #dcfce7 0%, #d1fae5 100%);
        border-color: #22c55e;
    }
    
    .step-icon {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        background: white;
        box-shadow: 0 1px 2px rgba(0,0,0,0.06);
    }
    
    .step-info {
        flex: 1;
    }
    
    .step-name {
        font-weight: 600;
        color: #1e293b;
        font-size: 0.95rem;
    }
    
    .step-status {
        font-size: 0.8rem;
        color: #64748b;
    }
    
    .step-badge {
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .badge-pending {
        background: #f1f5f9;
        color: #64748b;
    }
    
    .badge-active {
        background: #3b82f6;
        color: white;
    }
    
    .badge-done {
        background: #22c55e;
        color: white;
    }
    
    /* Score Display */
    .score-card {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 2px solid #22c55e;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
    }
    
    .score-value {
        font-size: 3.5rem;
        font-weight: 700;
        color: #16a34a;
        line-height: 1;
    }
    
    .score-label {
        color: #166534;
        font-size: 0.9rem;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        border-radius: 14px;
        padding: 1.25rem;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    
    .metric-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #1e293b;
    }
    
    .metric-label {
        color: #64748b;
        font-size: 0.8rem;
        font-weight: 500;
        margin-top: 0.25rem;
    }
    
    /* Input Styling */
    .stTextInput > div > div > input {
        background: white !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        color: #1e293b !important;
        padding: 0.875rem 1rem !important;
        font-size: 1rem !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #94a3b8 !important;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    }
    
    .stButton > button:disabled {
        background: #94a3b8 !important;
        box-shadow: none !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: white !important;
        border-right: 1px solid #e2e8f0;
    }
    
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #1e293b;
        font-size: 1rem;
        font-weight: 600;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: white !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        color: #1e293b !important;
    }
    
    .streamlit-expanderContent {
        background: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #f1f5f9;
        padding: 4px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: #64748b;
        font-weight: 500;
        padding: 0.5rem 1rem;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background: white !important;
        color: #1e293b !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.08);
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #3b82f6, #22c55e) !important;
        border-radius: 10px;
    }
    
    /* Info Box */
    .info-box {
        background: #f0f9ff;
        border: 1px solid #bae6fd;
        border-radius: 12px;
        padding: 1rem;
        color: #0369a1;
        font-size: 0.9rem;
    }
    
    /* Output Container */
    .output-box {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.25rem;
        margin: 0.75rem 0;
    }
    
    .output-header {
        display: flex;
        align-items: center;
        gap: 10px;
        padding-bottom: 0.75rem;
        margin-bottom: 0.75rem;
        border-bottom: 1px solid #f1f5f9;
    }
    
    .output-agent {
        font-weight: 600;
        color: #1e293b;
    }
    
    .output-time {
        color: #94a3b8;
        font-size: 0.8rem;
        margin-left: auto;
    }
    
    .output-content {
        color: #475569;
        font-size: 0.9rem;
        line-height: 1.7;
    }
    
    /* Section Header */
    .section-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 1.5rem 0 1rem 0;
    }
    
    .section-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1e293b;
    }
    
    /* Workflow Visualization */
    .workflow-container {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid #e2e8f0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.85rem;
        padding: 2rem 0 1rem 0;
        border-top: 1px solid #e2e8f0;
        margin-top: 2rem;
    }
    
    /* Divider */
    hr {
        border: none;
        border-top: 1px solid #e2e8f0;
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


def create_agent_workflow_chart(current_agent_idx: int = -1, completed_agents: list = None):
    """Create a clean visual representation of the agent workflow."""
    if completed_agents is None:
        completed_agents = []
    
    agents = get_agent_info()
    
    fig = go.Figure()
    
    x_positions = [0, 1, 2, 3]
    y_positions = [0, 0, 0, 0]
    
    colors = []
    for i, agent in enumerate(agents):
        if i in completed_agents:
            colors.append('#22c55e')  # Green
        elif i == current_agent_idx:
            colors.append('#3b82f6')  # Blue
        else:
            colors.append('#cbd5e1')  # Gray
    
    # Connecting lines
    for i in range(len(agents) - 1):
        line_color = '#22c55e' if i in completed_agents else '#e2e8f0'
        fig.add_trace(go.Scatter(
            x=[x_positions[i] + 0.12, x_positions[i + 1] - 0.12],
            y=[0, 0],
            mode='lines',
            line=dict(color=line_color, width=3),
            hoverinfo='skip',
            showlegend=False
        ))
    
    # Agent nodes
    fig.add_trace(go.Scatter(
        x=x_positions,
        y=y_positions,
        mode='markers+text',
        marker=dict(
            size=50,
            color=colors,
            line=dict(color='white', width=3),
            symbol='circle'
        ),
        text=[a['icon'] for a in agents],
        textposition='middle center',
        textfont=dict(size=20),
        hovertemplate='<b>%{customdata[0]}</b><br>%{customdata[1]}<extra></extra>',
        customdata=[[a['name'], a['role']] for a in agents],
        showlegend=False
    ))
    
    # Labels
    fig.add_trace(go.Scatter(
        x=x_positions,
        y=[-0.25] * 4,
        mode='text',
        text=[a['name'].replace('Collector', '').replace('Writer', '').replace('Optimizer', '').replace('Checker', '') for a in agents],
        textposition='bottom center',
        textfont=dict(size=11, color='#64748b', family='Plus Jakarta Sans'),
        hoverinfo='skip',
        showlegend=False
    ))
    
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.4, 3.4]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.5, 0.35]),
        margin=dict(l=10, r=10, t=10, b=10),
        height=140
    )
    
    return fig


def create_credibility_gauge(score: float):
    """Create a modern gauge chart for the overall score."""
    color = '#22c55e' if score >= 80 else '#f59e0b' if score >= 60 else '#ef4444'
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        number={'suffix': '%', 'font': {'size': 48, 'color': '#1e293b', 'family': 'Plus Jakarta Sans'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': '#e2e8f0', 'tickwidth': 1},
            'bar': {'color': color, 'thickness': 0.75},
            'bgcolor': '#f1f5f9',
            'borderwidth': 0,
            'steps': [
                {'range': [0, 60], 'color': '#fee2e2'},
                {'range': [60, 80], 'color': '#fef3c7'},
                {'range': [80, 100], 'color': '#dcfce7'}
            ],
            'threshold': {
                'line': {'color': color, 'width': 3},
                'thickness': 0.8,
                'value': score
            }
        }
    ))
    
    fig.update_layout(
        height=250,
        margin=dict(l=30, r=30, t=30, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Plus Jakarta Sans'}
    )
    
    return fig


def create_scores_bar_chart(scores: dict):
    """Create a horizontal bar chart for score breakdown."""
    labels = list(scores.keys())
    values = list(scores.values())
    
    colors = []
    for v in values:
        if v >= 80:
            colors.append('#22c55e')
        elif v >= 60:
            colors.append('#f59e0b')
        else:
            colors.append('#ef4444')
    
    fig = go.Figure(go.Bar(
        y=labels,
        x=values,
        orientation='h',
        marker=dict(
            color=colors,
            cornerradius=6
        ),
        text=[f'{v}%' for v in values],
        textposition='outside',
        textfont=dict(color='#475569', size=12, family='Plus Jakarta Sans')
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=True,
            gridcolor='#f1f5f9',
            range=[0, 110],
            tickfont=dict(color='#94a3b8', size=10)
        ),
        yaxis=dict(
            tickfont=dict(color='#475569', size=11, family='Plus Jakarta Sans'),
            showgrid=False
        ),
        margin=dict(l=120, r=40, t=20, b=20),
        height=200
    )
    
    return fig


def create_donut_chart(scores: dict):
    """Create a donut chart for score distribution."""
    labels = list(scores.keys())
    values = list(scores.values())
    colors = ['#3b82f6', '#8b5cf6', '#06b6d4', '#22c55e']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.65,
        marker=dict(colors=colors, line=dict(color='white', width=2)),
        textinfo='percent',
        textposition='outside',
        textfont=dict(size=11, color='#475569', family='Plus Jakarta Sans'),
        hovertemplate='<b>%{label}</b><br>Score: %{value}%<extra></extra>'
    )])
    
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.2,
            xanchor='center',
            x=0.5,
            font=dict(color='#475569', size=10, family='Plus Jakarta Sans')
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=20, b=50),
        height=280,
        annotations=[
            dict(
                text='<b>Score<br>Distribution</b>',
                x=0.5, y=0.5,
                font=dict(size=12, color='#64748b', family='Plus Jakarta Sans'),
                showarrow=False
            )
        ]
    )
    
    return fig


def extract_scores_from_response(response: str) -> dict:
    """Extract credibility scores from the fact checker's response."""
    scores = {
        'Factual Accuracy': 85,
        'Source Credibility': 80,
        'Content Quality': 88,
        'Timeliness': 90
    }
    
    patterns = [
        (r'Factual Accuracy[:\s|]*(\d+)%?', 'Factual Accuracy'),
        (r'Source Credibility[:\s|]*(\d+)%?', 'Source Credibility'),
        (r'Content Quality[:\s|]*(\d+)%?', 'Content Quality'),
        (r'Timeliness[:\s|]*(\d+)%?', 'Timeliness'),
    ]
    
    for pattern, key in patterns:
        match = re.search(pattern, response, re.IGNORECASE)
        if match:
            try:
                scores[key] = int(match.group(1))
            except ValueError:
                pass
    
    return scores


def calculate_overall_score(scores: dict) -> float:
    """Calculate weighted overall credibility score."""
    weights = {
        'Factual Accuracy': 0.40,
        'Source Credibility': 0.25,
        'Content Quality': 0.20,
        'Timeliness': 0.15
    }
    
    total = sum(scores.get(k, 0) * w for k, w in weights.items())
    return round(total, 1)


def main():
    """Main application function."""
    
    # Initialize session state
    if 'results' not in st.session_state:
        st.session_state.results = []
    if 'agent_outputs' not in st.session_state:
        st.session_state.agent_outputs = {}
    if 'is_running' not in st.session_state:
        st.session_state.is_running = False
    if 'completed_agents' not in st.session_state:
        st.session_state.completed_agents = []
    if 'current_agent' not in st.session_state:
        st.session_state.current_agent = -1
    
    # Header
    st.markdown('<h1 class="main-header">📊 ERP Trend Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Multi-Agent System for ERP Industry Intelligence</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🤖 Agent Pipeline")
        
        agents = get_agent_info()
        for i, agent in enumerate(agents):
            if i in st.session_state.completed_agents:
                status_class = "completed"
                badge_class = "badge-done"
                badge_text = "Done"
            elif i == st.session_state.current_agent:
                status_class = "active"
                badge_class = "badge-active"
                badge_text = "Active"
            else:
                status_class = ""
                badge_class = "badge-pending"
                badge_text = "Pending"
            
            st.markdown(f"""
            <div class="agent-step {status_class}">
                <div class="step-icon">{agent['icon']}</div>
                <div class="step-info">
                    <div class="step-name">{agent['name']}</div>
                    <div class="step-status">{agent['role']}</div>
                </div>
                <span class="step-badge {badge_class}">{badge_text}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### ℹ️ How It Works")
        st.markdown("""
        <div class="info-box">
            This system uses <b>4 AI agents</b> in a Round Robin pattern:
            <br><br>
            <b>1.</b> Research trends<br>
            <b>2.</b> Write content<br>
            <b>3.</b> Optimize for SEO<br>
            <b>4.</b> Verify accuracy
        </div>
        """, unsafe_allow_html=True)
    
    # Main Content
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### 🎯 Enter Your Topic")
        topic = st.text_input(
            "",
            placeholder="e.g., 'SAP S/4HANA Cloud trends' or leave empty for general ERP trends...",
            key="topic_input",
            label_visibility="collapsed"
        )
        
        if st.button("🚀 Analyze Trends", use_container_width=True, disabled=st.session_state.is_running):
            api_key = os.getenv("OPENAI_API_KEY", "")
            if not api_key or api_key == "your-openai-api-key-here":
                st.error("⚠️ Please set your OpenAI API key in the .env file!")
            else:
                st.session_state.is_running = True
                st.session_state.results = []
                st.session_state.agent_outputs = {}
                st.session_state.completed_agents = []
                st.session_state.current_agent = 0
                st.rerun()
    
    with col2:
        st.markdown("### 📈 Workflow Progress")
        fig = create_agent_workflow_chart(
            current_agent_idx=st.session_state.current_agent,
            completed_agents=st.session_state.completed_agents
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Processing Section
    if st.session_state.is_running:
        st.markdown("---")
        st.markdown("### ⚡ Processing...")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        agent_names = ['TrendCollector', 'ContentWriter', 'SEOOptimizer', 'FactChecker']
        output_containers = {}
        
        for agent_name in agent_names:
            with st.expander(f"📋 {agent_name} Output", expanded=False):
                output_containers[agent_name] = st.empty()
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            async def run_with_progress():
                team = await create_agent_team()
                task_topic = topic if topic else "Latest ERP Industry Trends and Developments"
                current_date = datetime.now().strftime('%B %d, %Y')
                task = f"""📅 **TODAY'S DATE: {current_date}**

Analyze the following topic for CURRENT and FUTURE trending news. Create optimized content.

⚠️ CRITICAL: Focus ONLY on:
- What's happening RIGHT NOW (December 2025)
- What's coming in 2026 and beyond
- DO NOT discuss past events or outdated trends

TOPIC: {task_topic}

Please work through the complete workflow:
1. TrendCollector: Research and identify the LATEST (2025) and UPCOMING (2026) trends
2. ContentWriter: Create engaging, forward-looking content
3. SEOOptimizer: Optimize with current year keywords (2025, 2026)
4. FactChecker: Verify accuracy and TIMELINESS (must be current/future, not past)

Begin the analysis now - remember we are at the END of 2025!"""
                
                results = []
                agent_outputs = {}
                completed = []
                
                async for message in team.run_stream(task=task):
                    if hasattr(message, 'source') and hasattr(message, 'content'):
                        source = message.source
                        content = message.content
                        
                        if source and content and source in agent_names:
                            current_idx = agent_names.index(source)
                            if current_idx not in completed:
                                completed.append(current_idx)
                            
                            agent_outputs[source] = content
                            results.append({
                                'agent': source,
                                'content': content,
                                'timestamp': datetime.now().strftime('%H:%M:%S')
                            })
                            
                            progress = len(completed) / len(agent_names)
                            progress_bar.progress(progress)
                            status_text.markdown(f"✨ **{source}** completed")
                            
                            if source in output_containers:
                                output_containers[source].markdown(content)
                
                return results, agent_outputs, completed
            
            results, agent_outputs, completed = loop.run_until_complete(run_with_progress())
            loop.close()
            
            st.session_state.results = results
            st.session_state.agent_outputs = agent_outputs
            st.session_state.completed_agents = completed
            st.session_state.is_running = False
            st.session_state.current_agent = -1
            
            progress_bar.progress(1.0)
            status_text.markdown("✅ **Analysis Complete!**")
            
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.session_state.is_running = False
    
    # Results Section
    if st.session_state.agent_outputs and not st.session_state.is_running:
        st.markdown("---")
        st.markdown("### 📊 Analysis Results")
        
        tab1, tab2, tab3 = st.tabs(["📝 Agent Outputs", "📈 Credibility Score", "📄 Full Report"])
        
        with tab1:
            for agent_name, output in st.session_state.agent_outputs.items():
                agent_info = next((a for a in get_agent_info() if a['name'] == agent_name), None)
                if agent_info:
                    with st.expander(f"{agent_info['icon']} {agent_name} — {agent_info['role']}", expanded=False):
                        st.markdown(output)
        
        with tab2:
            fact_checker_output = st.session_state.agent_outputs.get('FactChecker', '')
            scores = extract_scores_from_response(fact_checker_output)
            overall_score = calculate_overall_score(scores)
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                st.markdown("#### 🎯 Overall Score")
                gauge_fig = create_credibility_gauge(overall_score)
                st.plotly_chart(gauge_fig, use_container_width=True)
            
            with col2:
                st.markdown("#### 📊 Score Breakdown")
                bar_fig = create_scores_bar_chart(scores)
                st.plotly_chart(bar_fig, use_container_width=True)
            
            with col3:
                st.markdown("#### 🥧 Distribution")
                donut_fig = create_donut_chart(scores)
                st.plotly_chart(donut_fig, use_container_width=True)
            
            st.markdown("#### 📋 Detailed Metrics")
            metric_cols = st.columns(4)
            for i, (metric, value) in enumerate(scores.items()):
                with metric_cols[i]:
                    color = "#22c55e" if value >= 80 else "#f59e0b" if value >= 60 else "#ef4444"
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value" style="color: {color};">{value}%</div>
                        <div class="metric-label">{metric}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        with tab3:
            st.markdown("#### 📄 Complete Analysis Report")
            
            for result in st.session_state.results:
                agent_info = next((a for a in get_agent_info() if a['name'] == result['agent']), None)
                if agent_info:
                    st.markdown(f"""
                    <div class="output-box">
                        <div class="output-header">
                            <span style="font-size: 1.25rem;">{agent_info['icon']}</span>
                            <span class="output-agent">{result['agent']}</span>
                            <span class="output-time">🕐 {result['timestamp']}</span>
                        </div>
                        <div class="output-content">{result['content'][:3000]}{'...' if len(result['content']) > 3000 else ''}</div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        Built with ❤️ using <b>AutoGen</b> & <b>Streamlit</b><br>
        Multi-Agent System using Round Robin Group Chat
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
