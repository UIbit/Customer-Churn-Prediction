import streamlit as st
import pandas as pd
import pickle

st.set_page_config(
    page_title="ApexPulse Retention Studio",
    page_icon="📈",
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
        clr = verdict_color if is_verdict else "#1c1917"
        fw  = "700" if is_verdict else "400"
        html += (
            '<tr style="border-bottom:1px solid #f0f0f0;">'
            '<td style="font-size:12px;color:#9ca3af;padding:7px 0;width:120px;">' + str(key) + '</td>'
            '<td style="font-size:13px;color:' + clr + ';padding:7px 0;font-weight:' + fw + ';">' + str(val) + '</td>'
            '</tr>'
        )
    html += '</table>'
    return html

# Custom CSS - Version 2.0 (Cache Buster)
st.markdown("""
<style>
/* CACHE BUSTER v2.0 - Force refresh */
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

* {
    box-sizing: border-box !important;
}

html, body {
    max-width: 100% !important;
    overflow-x: hidden !important;
}

html, body, [class*="css"], .stApp {
    background: radial-gradient(circle at top left, rgba(14,165,233,0.10), transparent 30%), radial-gradient(circle at top right, rgba(20,184,166,0.10), transparent 24%), linear-gradient(180deg, #f8fafc 0%, #eef4f8 100%) !important;
    color: #0f172a !important;
    font-family: 'Manrope', sans-serif !important;
}

#MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stSidebar"], .stDeployButton {
    display: none !important;
}

.block-container, [data-testid="block-container"] {
    padding: 0 !important; 
    max-width: 100% !important;
}

[data-testid="stVerticalBlock"] { gap: 0 !important; }
.element-container, .stMarkdown { margin: 0 !important; padding: 0 !important; }

/* Responsive container class */
.responsive-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
    width: 100%;
}

@media (min-width: 768px) {
    .responsive-container {
        padding: 0 2rem;
    }
}

@media (min-width: 1024px) {
    .responsive-container {
        padding: 0 3rem;
    }
}

/* Form controls styling */
div[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.92) !important;
    border: 1px solid #d7e0ea !important;
    border-radius: 14px !important;
    color: #0f172a !important;
    font-family: 'Manrope', sans-serif !important;
    font-size: 14px !important;
}

div[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.92) !important;
    border: 1px solid #d7e0ea !important;
    border-radius: 14px !important;
    color: #0f172a !important;
    font-family: 'Manrope', sans-serif !important;
    font-size: 14px !important;
}

[data-testid="stSlider"] {
    padding: 0.5rem 0;
}

[data-testid="stRadio"] > div {
    display: flex !important;
    flex-direction: row !important;
    gap: 8px !important;
    flex-wrap: wrap !important;
}

[data-testid="stRadio"] label {
    flex: 1 !important;
    min-width: 80px !important;
    padding: 9px 14px !important;
    background: rgba(255,255,255,0.92) !important;
    border: 1px solid #d7e0ea !important;
    border-radius: 14px !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    transition: all 0.15s !important;
}

[data-testid="stButton"] > button {
    width: 100% !important; 
    padding: 14px !important;
    background: linear-gradient(135deg, #0f172a 0%, #0ea5e9 55%, #14b8a6 100%) !important; 
    color: #ffffff !important;
    font-family: 'Manrope', sans-serif !important;
    font-size: 14px !important; 
    font-weight: 600 !important;
    border: none !important; 
    border-radius: 14px !important;
    cursor: pointer !important; 
    margin-top: 24px !important;
    transition: all 0.15s ease !important;
}

[data-testid="stButton"] > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 10px 24px rgba(15,23,42,0.16) !important;
}

.glass-card {
    background: rgba(255,255,255,0.82);
    backdrop-filter: blur(18px);
    border: 1px solid rgba(148,163,184,0.18);
    box-shadow: 0 18px 45px rgba(15,23,42,0.06);
    border-radius: 18px;
    padding: 16px;
    box-sizing: border-box;
    word-wrap: break-word;
    overflow-wrap: anywhere;
}

/* Responsive text handling */
.glass-card * {
    word-break: break-word;
    overflow-wrap: anywhere;
}

/* Column responsive behavior */
[data-testid="column"] {
    padding: 0 0.5rem !important;
}

@media (max-width: 768px) {
    [data-testid="column"] {
        padding: 0 0.25rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

# Navigation Header
st.markdown("""
<div style="background:rgba(255,255,255,0.74); border-bottom:1px solid rgba(148,163,184,0.18);">
  <div class="responsive-container" style="display:flex; justify-content:space-between; align-items:center; height:64px;">
    <div style="display:flex; align-items:center; gap:10px;">
      <div style="width:32px; height:32px; background:linear-gradient(135deg, #0ea5e9, #14b8a6); border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:15px;">🏦</div>
      <div>
        <div style="font-size:16px; font-weight:800; color:#0f172a;">Apex<span style="color:#0ea5e9;">Pulse</span></div>
        <div style="font-size:11px; color:#64748b;">Customer retention studio</div>
      </div>
    </div>
    <div style="display:flex; align-items:center; gap:6px; padding:6px 14px; background:rgba(236,253,245,0.95); border:1px solid #bbf7d0; border-radius:999px;">
      <span style="width:7px; height:7px; background:#10b981; border-radius:50%; display:inline-block;"></span>
      <span style="font-size:12px; font-weight:600; color:#047857;">Model Ready</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div style="background:linear-gradient(135deg, #0f172a 0%, #0b3b61 52%, #0f766e 100%);">
  <div class="responsive-container" style="padding-top:44px; padding-bottom:40px;">
    <div style="font-size:12px; font-weight:600; color:#a5f3fc; margin-bottom:12px; letter-spacing:1px; text-transform:uppercase;">Client retention intelligence</div>
    <div style="font-size:clamp(24px,4vw,48px); font-weight:800; color:#ffffff; line-height:1.1; margin-bottom:12px;">
        Spot churn signals early<br><span style="color:#67e8f9;">and act with confidence.</span>
    </div>
    <div style="max-width:720px; font-size:15px; line-height:1.7; color:#dbeafe;">
        A polished banking risk dashboard for comparing customer profiles, estimating churn probability, and suggesting the next best action.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# Stats Section
st.markdown("""
<div style='background:#1e3a8a;'>
  <div class="responsive-container">
""", unsafe_allow_html=True)

sc1, sc2, sc3, sc4 = st.columns(4)
stats = [
    (sc1, "10,000", "Profiles analysed", "Training dataset size", False),
    (sc2, "86.6%", "Model accuracy", "Random Forest", True),
    (sc3, "3", "Models compared", "LR - DT - RF", False),
    (sc4, "~20%", "Typical churn rate", "Industry baseline", False),
]

for col, num, label, sub, hi in stats:
    # Improved contrast colors for better readability
    num_color = '#ffffff' if hi else '#e2e8f0'
    label_color = '#f1f5f9'
    sub_color = '#cbd5e1'
    
    col.markdown(f"""
        <div style="padding:20px 0 24px; border-right:1px solid rgba(255,255,255,0.08); text-align:center;">
            <div style="font-size:clamp(24px, 5vw, 30px); font-weight:800; color:{num_color}; margin-bottom:6px;">{num}</div>
            <div style="font-size:13px; font-weight:600; color:{label_color}; margin-bottom:2px;">{label}</div>
            <div style="font-size:11px; color:{sub_color};">{sub}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
  </div>
</div>
""", unsafe_allow_html=True)

# Main Content
st.markdown("""
<div style='background:#f8f9fa;'>
  <div class="responsive-container" style="padding-top:36px; padding-bottom:36px;">
""", unsafe_allow_html=True)

# Create responsive columns that stack on mobile
col1, col2 = st.columns([1, 1], gap="large")

# Left Column - Input Form
with col1:
    st.markdown("""
        <div style="font-size:13px; font-weight:700; color:#0ea5e9; padding-bottom:10px; border-bottom:2px solid #0ea5e9; margin-bottom:20px;">
            Step 1 - Enter customer details
        </div>
    """, unsafe_allow_html=True)

    # Personal Information
    st.markdown("**👤 Personal Information**")
    c1, c2 = st.columns(2)
    with c1: geography = st.selectbox("Country", le_geo.classes_)
    with c2: gender = st.selectbox("Gender", le_gen.classes_)

    c3, c4 = st.columns(2)
    with c3: age = st.slider("Age", 18, 92, 38)
    with c4: tenure = st.slider("Tenure (Years)", 0, 10, 5)

    # Financial Information
    st.markdown("**💰 Financial Information**")
    c5, c6 = st.columns(2)
    with c5:
        credit_score = st.slider("Credit Score", 300, 850, 650)
        balance = st.number_input("Account Balance ($)", 0.0, value=76000.0, step=500.0)
    with c6:
        num_products = st.selectbox("Number of Products", [1, 2, 3, 4])
        estimated_salary = st.number_input("Annual Salary ($)", 0.0, value=85000.0, step=500.0)

    # Account Details
    st.markdown("**🏦 Account Details**")
    c7, c8 = st.columns(2)
    with c7: has_cr_card = st.radio("Has Credit Card?", ["Yes", "No"], horizontal=True)
    with c8: is_active = st.radio("Active Member?", ["Yes", "No"], horizontal=True)

    predict = st.button("🔮 Generate Risk Forecast", use_container_width=True)

# Right Column - Results
with col2:
    st.markdown("""
        <div style="font-size:13px; font-weight:700; color:#0ea5e9; padding-bottom:10px; border-bottom:2px solid #0ea5e9; margin-bottom:24px;">
            Step 2 - View prediction result
        </div>
    """, unsafe_allow_html=True)

    if not predict:
        st.markdown("""
            <div class="glass-card" style="text-align:center; margin-bottom:16px; padding:52px 32px;">
                <div style="font-size:36px; margin-bottom:12px; opacity:0.3;">🏦</div>
                <div style="font-size:16px; font-weight:600; color:#374151; margin-bottom:8px;">Waiting for inputs</div>
                <div style="font-size:13px; color:#9ca3af; line-height:1.6;">
                    Enter the customer profile on the left<br>and generate the forecast here.
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Key insights
        st.markdown("**📊 Key Training Insights**")
        facts = [
            ("📍", "Germany has the highest churn rate among all 3 countries."),
            ("👥", "Customers aged 40-60 are most likely to leave the bank."),
            ("📦", "Customers with only 1 product churn significantly more."),
            ("⚡", "Inactive members are 3x more likely to churn."),
        ]
        for icon, text in facts:
            st.markdown(f"""
                <div class="glass-card" style="display:flex; align-items:flex-start; gap:10px; padding:12px; margin-bottom:8px;">
                    <span style="font-size:16px; flex-shrink:0;">{icon}</span>
                    <span style="font-size:13px; color:#334155; line-height:1.5;">{text}</span>
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
        stay = 100 - pct

        if prediction == 1:
            risk_level = "HIGH RISK"
            risk_color = "#e11d48"
            bg_color = "#fff1f2"
            border_color = "#fda4af"
            advice = "This customer is likely to leave. Immediate intervention recommended."
            actions = [
                ("📞", "Contact immediately", "Assign a relationship manager within 24 hours"),
                ("💸", "Offer better rates", "Present personalized rate revision or fee waiver"),
                ("📦", "Bundle products", "Offer additional products to improve stickiness"),
                ("💬", "Get feedback", "Schedule satisfaction review call"),
            ]
        else:
            risk_level = "LOW RISK"
            risk_color = "#059669"
            bg_color = "#ecfdf5"
            border_color = "#86efac"
            advice = "This customer is stable. Focus on growth opportunities."
            actions = [
                ("📈", "Upsell products", "Identify premium products they might need"),
                ("🏆", "Upgrade tier", "Enroll in loyalty or rewards program"),
                ("💡", "Wealth advisory", "Suggest investment consultation"),
                ("📋", "Regular check-in", "Schedule quarterly satisfaction call"),
            ]

        # Results display with improved responsive design
        st.markdown(f"""
            <div class="glass-card" style="background:{bg_color}; border:1px solid {border_color}; border-left:4px solid {risk_color}; margin-bottom:16px; padding:24px;">
                <div style="font-size:13px; color:{risk_color}; font-weight:700; margin-bottom:6px; text-transform:uppercase;">
                    ⚠️ {risk_level}
                </div>
                <div style="font-size:clamp(18px, 4vw, 22px); font-weight:800; color:#0f172a; margin-bottom:6px; line-height:1.2;">
                    {pct}% Churn Probability
                </div>
                <div style="font-size:13px; color:#475569; margin-bottom:16px;">{advice}</div>
                <div style="height:8px; background:#e2e8f0; border-radius:999px; overflow:hidden;">
                    <div style="height:8px; width:{pct}%; background:{risk_color}; border-radius:999px; transition: width 0.5s ease;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Metrics with improved responsive design
        mx1, mx2, mx3, mx4 = st.columns(4)
        metrics = [
            (mx1, f"{pct}%", "Churn Risk", risk_color),
            (mx2, f"{stay}%", "Will Stay", "#16a34a"),
            (mx3, "RF", "Model", "#0ea5e9"),
            (mx4, "86.6%", "Accuracy", "#0ea5e9"),
        ]
        for col, val, lbl, clr in metrics:
            col.markdown(f"""
                <div class="glass-card" style="text-align:center; margin-bottom:14px; padding:12px 8px;">
                    <div style="font-size:clamp(16px, 4vw, 20px); font-weight:800; color:{clr}; margin-bottom:4px;">{val}</div>
                    <div style="font-size:10px; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">{lbl}</div>
                </div>
            """, unsafe_allow_html=True)

        # Customer Summary & Actions with better responsive layout
        st.markdown("### 📋 Customer Summary")
        
        rows = [
            ("Country", geography, False),
            ("Gender", gender, False),
            ("Age", f"{age} years", False),
            ("Tenure", f"{tenure} years", False),
            ("Credit Score", str(credit_score), False),
            ("Balance", f"${balance:,.0f}", False),
            ("Products", str(num_products), False),
            ("Credit Card", has_cr_card, False),
            ("Active", is_active, False),
            ("Risk Level", risk_level, True),
        ]
        table_html = build_table(rows, risk_color)
        st.markdown(f'<div class="glass-card">{table_html}</div>', unsafe_allow_html=True)
        
        st.markdown("### 🎯 Recommended Actions")
        
        # Improved action rendering - clean, structured format
        for i, (emoji, title, desc) in enumerate(actions):
            st.markdown(f"""
                <div class="glass-card" style="margin-bottom:12px; padding:16px;">
                    <div style="display:flex; align-items:flex-start; gap:12px;">
                        <span style="font-size:20px; flex-shrink:0; margin-top:2px;">{emoji}</span>
                        <div style="flex:1;">
                            <div style="font-size:14px; font-weight:600; color:#1a202c; margin-bottom:4px; line-height:1.3;">{title}</div>
                            <div style="font-size:12px; color:#4a5568; line-height:1.4;">{desc}</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# Close the main content container
st.markdown("""
  </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="border-top:1px solid #e2e8f0;">
  <div class="responsive-container" style="padding-top:28px; padding-bottom:28px; text-align:center; color:#64748b; font-size:12px;">
    ApexPulse Customer Churn Prediction Dashboard • Powered by Machine Learning
  </div>
</div>
""", unsafe_allow_html=True)