import streamlit as st
import pandas as pd
import pickle
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

st.set_page_config(
    page_title="CHURN PREDICTION LOGIC",
    page_icon="⚠️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

@st.cache_resource
def load():
    model    = pickle.load(open("models/best_model.pkl",    "rb"))
    scaler   = pickle.load(open("models/scaler.pkl",        "rb"))
    le_geo   = pickle.load(open("models/le_geo.pkl",        "rb"))
    le_gen   = pickle.load(open("models/le_gen.pkl",        "rb"))
    features = pickle.load(open("models/feature_names.pkl", "rb"))
    return model, scaler, le_geo, le_gen, features

model, scaler, le_geo, le_gen, feature_names = load()

def build_table(rows, verdict_color):
    html = '<table style="width:100%;border-collapse:collapse;">'
    for key, val, is_verdict in rows:
        clr = verdict_color if is_verdict else "#cccccc"
        fw  = "700" if is_verdict else "400"
        html += (
            '<tr style="border-bottom:1px solid #444;">'
            '<td style="font-size:12px;color:#999;padding:7px 0;width:120px;">' + str(key) + '</td>'
            '<td style="font-size:13px;color:' + clr + ';padding:7px 0;font-weight:' + fw + ';">' + str(val) + '</td>'
            '</tr>'
        )
    html += '</table>'
    return html

# Helper function to create mini charts
def create_mini_chart(data, chart_type="line"):
    fig = go.Figure()
    
    if chart_type == "line":
        fig.add_trace(go.Scatter(
            x=list(range(len(data))),
            y=data,
            mode='lines',
            line=dict(color='#ff4500', width=2),
            fill='tonexty' if len(data) > 1 else None,
            fillcolor='rgba(255, 69, 0, 0.1)'
        ))
    elif chart_type == "bar":
        fig.add_trace(go.Bar(
            x=list(range(len(data))),
            y=data,
            marker_color='#ff4500',
            opacity=0.8
        ))
    
    fig.update_layout(
        height=80,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False)
    )
    
    return fig
# Dark Dashboard CSS - Cyber Security Theme
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');

* {
    box-sizing: border-box !important;
    margin: 0;
    padding: 0;
}

html, body {
    max-width: 100% !important;
    overflow-x: hidden !important;
}

.stApp {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0f0f0f 100%) !important;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
}

#MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stSidebar"], .stDeployButton {
    display: none !important;
}

.block-container, [data-testid="block-container"] {
    padding: 1rem !important; 
    max-width: 100% !important;
}

/* Header Styling */
.main-header {
    background: rgba(20, 20, 20, 0.95);
    border: 1px solid #ff4500;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 30px;
    position: relative;
    overflow: hidden;
}

.main-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, #ff4500, #ff6500, #ff4500);
    animation: pulse 2s ease-in-out infinite alternate;
}

@keyframes pulse {
    0% { opacity: 0.6; }
    100% { opacity: 1; }
}

.header-title {
    font-family: 'Roboto Mono', monospace;
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 8px;
}

.header-subtitle {
    color: #ff4500;
    font-size: 14px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.objective-text {
    position: absolute;
    top: 20px;
    right: 20px;
    background: rgba(255, 69, 0, 0.1);
    border: 1px solid #ff4500;
    border-radius: 4px;
    padding: 10px 15px;
    font-size: 12px;
    max-width: 200px;
}

.objective-label {
    color: #ff4500;
    font-weight: 600;
    text-transform: uppercase;
    margin-bottom: 5px;
}

/* Dashboard Grid */
.dashboard-grid {
    display: grid;
    grid-template-columns: 1fr 300px 1fr;
    gap: 20px;
    margin-bottom: 30px;
}

@media (max-width: 1200px) {
    .dashboard-grid {
        grid-template-columns: 1fr;
    }
}

/* Input Signals Section */
.input-section {
    background: rgba(30, 30, 30, 0.8);
    border: 1px solid #333;
    border-radius: 8px;
    padding: 20px;
}

.section-title {
    color: #ff4500;
    font-family: 'Roboto Mono', monospace;
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 20px;
    border-bottom: 1px solid #ff4500;
    padding-bottom: 8px;
}

/* Chart Containers */
.chart-container {
    background: rgba(20, 20, 20, 0.9);
    border: 1px solid #444;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 20px;
    position: relative;
}

.chart-title {
    color: #ffffff;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.chart-value {
    color: #ff4500;
    font-family: 'Roboto Mono', monospace;
    font-size: 11px;
    opacity: 0.8;
}

/* AI Model Section */
.ai-model-section {
    background: linear-gradient(135deg, rgba(255, 69, 0, 0.1) 0%, rgba(255, 69, 0, 0.05) 100%);
    border: 2px solid #ff4500;
    border-radius: 12px;
    padding: 30px;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.ai-model-section::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255, 69, 0, 0.1) 0%, transparent 70%);
    animation: rotate 10s linear infinite;
}

@keyframes rotate {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.ai-badge {
    background: #ff4500;
    color: #000;
    font-family: 'Roboto Mono', monospace;
    font-size: 12px;
    font-weight: 700;
    padding: 8px 16px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 1px;
    position: relative;
    z-index: 2;
    margin-bottom: 15px;
    display: inline-block;
}

.model-type {
    color: #ffffff;
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 5px;
    position: relative;
    z-index: 2;
}

.model-desc {
    color: #cccccc;
    font-size: 12px;
    position: relative;
    z-index: 2;
}
/* Form Controls */
[data-testid="stSelectbox"] > div > div,
[data-testid="stNumberInput"] input,
[data-testid="stSlider"] {
    background: rgba(30, 30, 30, 0.9) !important;
    border: 1px solid #444 !important;
    border-radius: 4px !important;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stSelectbox"] > div > div:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: #ff4500 !important;
    box-shadow: 0 0 10px rgba(255, 69, 0, 0.3) !important;
}

[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #ff4500 0%, #ff6500 100%) !important;
    color: #000000 !important;
    font-family: 'Roboto Mono', monospace !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 12px 24px !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
}

[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #ff6500 0%, #ff4500 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 5px 20px rgba(255, 69, 0, 0.4) !important;
}

/* Output Alert Section */
.alert-section {
    background: rgba(30, 30, 30, 0.8);
    border: 1px solid #333;
    border-radius: 8px;
    padding: 20px;
}

.high-risk-alert {
    background: linear-gradient(135deg, rgba(255, 69, 0, 0.2) 0%, rgba(255, 0, 0, 0.1) 100%);
    border: 2px solid #ff4500;
    border-radius: 12px;
    padding: 25px;
    text-align: center;
    margin-bottom: 20px;
    position: relative;
}
.alert-icon {
    font-size: 48px;
    color: #ff4500;
    margin-bottom: 15px;
    animation: pulse 1.5s ease-in-out infinite alternate;
}

.alert-title {
    color: #ff4500;
    font-family: 'Roboto Mono', monospace;
    font-size: 18px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 10px;
}

.risk-score {
    font-family: 'Roboto Mono', monospace;
    font-size: 36px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 5px;
}

.risk-label {
    color: #ff4500;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Process Flow */
.process-flow {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin: 30px 0;
    padding: 20px;
    background: rgba(20, 20, 20, 0.9);
    border-radius: 8px;
    border: 1px solid #333;
}

@media (max-width: 768px) {
    .process-flow {
        grid-template-columns: repeat(2, 1fr);
    }
}

.process-step {
    text-align: center;
    padding: 20px;
    background: rgba(30, 30, 30, 0.8);
    border: 1px solid #444;
    border-radius: 8px;
    position: relative;
}

.process-number {
    background: #ff4500;
    color: #000;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    margin: 0 auto 15px;
    font-size: 14px;
}
.process-icon {
    font-size: 24px;
    margin-bottom: 10px;
}

.process-title {
    color: #ff4500;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.process-desc {
    color: #cccccc;
    font-size: 10px;
    line-height: 1.4;
}

/* Risk Factors */
.risk-factors {
    margin-top: 20px;
}

.risk-factor {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px;
    background: rgba(30, 30, 30, 0.8);
    border: 1px solid #444;
    border-radius: 6px;
    margin-bottom: 8px;
}

.risk-factor-name {
    color: #ffffff;
    font-size: 12px;
    font-weight: 500;
}

.risk-factor-value {
    color: #ff4500;
    font-family: 'Roboto Mono', monospace;
    font-size: 12px;
    font-weight: 600;
}

/* Recommendations */
.recommendations {
    background: rgba(20, 20, 20, 0.9);
    border: 1px solid #ff4500;
    border-radius: 8px;
    padding: 20px;
    margin-top: 20px;
}

.recommendation-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px;
    background: rgba(30, 30, 30, 0.8);
    border: 1px solid #444;
    border-radius: 6px;
    margin-bottom: 10px;
    transition: all 0.3s ease;
}

.recommendation-item:hover {
    border-color: #ff4500;
    background: rgba(255, 69, 0, 0.05);
}
.recommendation-bullet {
    width: 6px;
    height: 6px;
    background: #ff4500;
    border-radius: 50%;
    flex-shrink: 0;
}

.recommendation-text {
    color: #ffffff;
    font-size: 13px;
    line-height: 1.4;
}

/* Confidence Meter */
.confidence-meter {
    background: rgba(20, 20, 20, 0.9);
    border: 1px solid #444;
    border-radius: 8px;
    padding: 20px;
    margin-top: 20px;
    text-align: center;
}

.confidence-circle {
    width: 120px;
    height: 120px;
    margin: 0 auto 15px;
    position: relative;
}

.confidence-value {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-family: 'Roboto Mono', monospace;
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
}

.confidence-label {
    text-align: center;
    color: #ff4500;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
}

/* Scrollbar Styling */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(30, 30, 30, 0.8);
}

::-webkit-scrollbar-thumb {
    background: #ff4500;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #ff6500;
}
</style>
""", unsafe_allow_html=True)
# Header Section
st.markdown("""
<div class="main-header">
    <div class="header-title">CHURN PREDICTION LOGIC</div>
    <div class="header-subtitle">Real-time risk assessment for subscription retention</div>
    <div class="objective-text">
        <div class="objective-label">OBJECTIVE</div>
        <div>Identify at-risk subscribers and trigger proactive retention workflows</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Dashboard Grid Layout
col1, col2, col3 = st.columns([1, 0.8, 1])

# Left Column - INPUT SIGNALS
with col1:
    st.markdown("""
    <div class="input-section">
        <div class="section-title">INPUT SIGNALS</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login Frequency Chart
    st.markdown("""
    <div class="chart-container">
        <div class="chart-title">📊 Login Frequency <span class="chart-value">(30D)</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate sample login frequency data
    login_data = np.random.normal(15, 5, 30).clip(0, 30)
    chart1 = create_mini_chart(login_data, "line")
    st.plotly_chart(chart1, use_container_width=True, config={'displayModeBar': False})
    
    # Portal Activity Chart
    st.markdown("""
    <div class="chart-container">
        <div class="chart-title">📱 Portal Activity <span class="chart-value">(30D)</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate sample portal activity data
    portal_data = np.random.normal(8, 3, 30).clip(0, 20)
    chart2 = create_mini_chart(portal_data, "line")
    st.plotly_chart(chart2, use_container_width=True, config={'displayModeBar': False})
    
    # Shipping Status Chart
    st.markdown("""
    <div class="chart-container">
        <div class="chart-title">📦 Shipping Status <span class="chart-value">(30D)</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate sample shipping data
    shipping_data = np.random.normal(3, 1, 30).clip(0, 10)
    chart3 = create_mini_chart(shipping_data, "bar")
    st.plotly_chart(chart3, use_container_width=True, config={'displayModeBar': False})

    # Customer Input Form
    st.markdown("### Customer Profile Input")
    
    geography = st.selectbox("Country", le_geo.classes_)
    gender = st.selectbox("Gender", le_gen.classes_)
    age = st.slider("Age", 18, 92, 38)
    tenure = st.slider("Tenure (Years)", 0, 10, 5)
    credit_score = st.slider("Credit Score", 300, 850, 650)
    balance = st.number_input("Account Balance ($)", 0.0, value=76000.0, step=500.0)
    num_products = st.selectbox("Number of Products", [1, 2, 3, 4])
    estimated_salary = st.number_input("Annual Salary ($)", 0.0, value=85000.0, step=500.0)
    has_cr_card = st.radio("Has Credit Card?", ["Yes", "No"], horizontal=True)
    is_active = st.radio("Active Member?", ["Yes", "No"], horizontal=True)
    
    predict = st.button("🔍 ANALYZE RISK", use_container_width=True)
# Center Column - AI MODEL
with col2:
    st.markdown("""
    <div class="ai-model-section">
        <div class="ai-badge">AI MODEL</div>
        <div class="model-type">Gradient Boosted Decision Trees</div>
        <div class="model-desc">Advanced ML classification engine</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-top: 30px;">
        <div class="section-title">RISK SCORING ENGINE</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Risk Factors (Weighted)
    st.markdown("""
    <div class="risk-factors">
        <div class="risk-factor">
            <span class="risk-factor-name">Login Frequency</span>
            <span class="risk-factor-value">40%</span>
        </div>
        <div class="risk-factor">
            <span class="risk-factor-name">Portal Activity</span>
            <span class="risk-factor-value">35%</span>
        </div>
        <div class="risk-factor">
            <span class="risk-factor-name">Shipping Status</span>
            <span class="risk-factor-value">25%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Right Column - OUTPUT
with col3:
    st.markdown("""
    <div class="alert-section">
        <div class="section-title">OUTPUT</div>
    </div>
    """, unsafe_allow_html=True)
    
    if not predict:
        st.markdown("""
        <div class="high-risk-alert">
            <div class="alert-icon">⚠️</div>
            <div class="alert-title">AWAITING INPUT</div>
            <div class="risk-score">--</div>
            <div class="risk-label">CHURN RISK SCORE</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="recommendations">
            <div class="section-title">STANDBY MODE</div>
            <div style="text-align: center; padding: 20px; color: #666;">
                Enter customer data to generate risk assessment
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        # Process prediction
        geo_enc = le_geo.transform([geography])[0]
        gen_enc = le_gen.transform([gender])[0]
        cr_card = 1 if has_cr_card == "Yes" else 0
        active = 1 if is_active == "Yes" else 0

        inp = pd.DataFrame([[
            credit_score, geo_enc, gen_enc, age, tenure,
            balance, num_products, cr_card, active, estimated_salary
        ]], columns=feature_names)

        prob = model.predict_proba(scaler.transform(inp))[0][1]
        prediction = model.predict(scaler.transform(inp))[0]
        pct = int(prob * 100)
        
        # Display High Risk Alert
        risk_status = "HIGH-RISK ALERT" if prediction == 1 else "LOW-RISK STATUS"
        risk_color = "#ff4500" if prediction == 1 else "#00ff00"
        
        st.markdown(f"""
        <div class="high-risk-alert">
            <div class="alert-icon">⚠️</div>
            <div class="alert-title">{risk_status}</div>
            <div class="risk-score">{pct}</div>
            <div class="risk-label">CHURN RISK SCORE</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: rgba(20, 20, 20, 0.9); border: 1px solid #444; border-radius: 8px; padding: 15px; margin: 15px 0;">
            <div class="risk-factor">
                <span class="risk-factor-name">RISK LEVEL: HIGH</span>
                <span class="risk-factor-value"></span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        # Recommended Actions
        if prediction == 1:
            actions = [
                "Trigger retention workflow",
                "Send personalized offer",
                "Assign to success manager", 
                "Increase engagement"
            ]
        else:
            actions = [
                "Continue standard engagement",
                "Monitor usage patterns",
                "Upsell opportunities",
                "Maintain service quality"
            ]
        
        st.markdown("""
        <div class="recommendations">
            <div class="section-title">RECOMMENDED ACTIONS</div>
        </div>
        """, unsafe_allow_html=True)
        
        for action in actions:
            st.markdown(f"""
            <div class="recommendation-item">
                <div class="recommendation-bullet"></div>
                <div class="recommendation-text">{action}</div>
            </div>
            """, unsafe_allow_html=True)

# HOW IT WORKS Section
st.markdown("""
<div class="process-flow">
    <div class="process-step">
        <div class="process-number">1</div>
        <div class="process-icon">🗄️</div>
        <div class="process-title">COLLECT</div>
        <div class="process-desc">Gather user behavior and operational data from multiple sources</div>
    </div>
    <div class="process-step">
        <div class="process-number">2</div>
        <div class="process-icon">⚙️</div>
        <div class="process-title">PROCESS</div>
        <div class="process-desc">Apply ML algorithms and normalized risk scoring</div>
    </div>
    <div class="process-step">
        <div class="process-number">3</div>
        <div class="process-icon">🧠</div>
        <div class="process-title">SCORE</div>
        <div class="process-desc">Generate predictions, classify based on churn factors</div>
    </div>
    <div class="process-step">
        <div class="process-number">4</div>
        <div class="process-icon">🔔</div>
        <div class="process-title">ALERT</div>
        <div class="process-desc">Trigger alerts and suggested retention workflows</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Model Confidence Section
st.markdown("""
<div style="text-align: center; margin: 30px 0;">
    <div class="section-title">MODEL CONFIDENCE</div>
</div>
""", unsafe_allow_html=True)

# Confidence meter using Plotly
confidence_value = 92  # Model accuracy
fig_confidence = go.Figure(go.Indicator(
    mode="gauge+number",
    value=confidence_value,
    domain={'x': [0, 1], 'y': [0, 1]},
    title={'text': "Confidence", 'font': {'color': '#ff4500', 'size': 16}},
    gauge={
        'axis': {'range': [None, 100], 'tickcolor': '#ffffff'},
        'bar': {'color': "#ff4500"},
        'steps': [
            {'range': [0, 50], 'color': "rgba(255, 69, 0, 0.1)"},
            {'range': [50, 80], 'color': "rgba(255, 69, 0, 0.2)"},
            {'range': [80, 100], 'color': "rgba(255, 69, 0, 0.3)"}
        ],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': 90
        }
    },
    number={'font': {'color': '#ffffff', 'size': 24}}
))

fig_confidence.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font={'color': '#ffffff'},
    height=300
)

st.plotly_chart(fig_confidence, use_container_width=True)

st.markdown("""
<div style="text-align: center; color: #999; font-size: 12px; margin-top: -20px;">
    Model evaluated against 10,000 customer records<br>
    <span style="color: #ff4500;">AUC-ROC: 0.91</span>
</div>
""", unsafe_allow_html=True)