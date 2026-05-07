import streamlit as st
import pandas as pd
import pickle

st.set_page_config(
    page_title="ApexPulse · Retention Studio",
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

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {
    background:
        radial-gradient(circle at top left, rgba(14,165,233,0.10), transparent 30%),
        radial-gradient(circle at top right, rgba(20,184,166,0.10), transparent 24%),
        linear-gradient(180deg, #f8fafc 0%, #eef4f8 100%) !important;
    color: #0f172a !important;
    font-family: 'Manrope', sans-serif !important;
}

#MainMenu, footer, header,
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stSidebar"], .stDeployButton {
    display: none !important;
}

.block-container, [data-testid="block-container"] {
    padding: 0 !important; max-width: 100% !important;
}
[data-testid="stVerticalBlock"] { gap: 0 !important; }
.element-container, .stMarkdown { margin: 0 !important; padding: 0 !important; }

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    pointer-events: none;
    background-image: linear-gradient(rgba(15,23,42,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(15,23,42,0.03) 1px, transparent 1px);
    background-size: 72px 72px;
    mask-image: linear-gradient(180deg, rgba(0,0,0,0.28), transparent 78%);
    z-index: 0;
}

.stApp > div {
    position: relative;
    z-index: 1;
}

/* LABELS */
div[data-testid="stSelectbox"] label p,
div[data-testid="stNumberInput"] label p,
div[data-testid="stSlider"] label p,
div[data-testid="stRadio"] label p,
[data-testid="stWidgetLabel"] p {
    font-family: 'Manrope', sans-serif !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    color: #475569 !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
    margin-top: 14px !important;
    margin-bottom: 5px !important;
}

/* SELECTBOX */
div[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.92) !important;
    border: 1px solid #d7e0ea !important;
    border-radius: 14px !important;
    color: #0f172a !important;
    font-family: 'Manrope', sans-serif !important;
    font-size: 14px !important;
}
div[data-testid="stSelectbox"] > div > div:hover { border-color: #0ea5e9 !important; }
div[data-testid="stSelectbox"] span { color: #0f172a !important; }
div[data-testid="stSelectbox"] svg  { fill: #9ca3af !important; }
[data-baseweb="popover"] [role="option"] {
    background: #ffffff !important; color: #0f172a !important;
}
[data-baseweb="popover"] [role="option"]:hover { background: #ecfeff !important; }

/* NUMBER INPUT */
div[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.92) !important;
    border: 1px solid #d7e0ea !important;
    border-radius: 14px !important;
    color: #0f172a !important;
    font-family: 'Manrope', sans-serif !important;
    font-size: 14px !important;
}
div[data-testid="stNumberInput"] input:focus {
    border-color: #0ea5e9 !important;
    outline: none !important;
    box-shadow: 0 0 0 3px rgba(14,165,233,0.10) !important;
}
div[data-testid="stNumberInput"] button {
    background: #ffffff !important;
    border: 1px solid #d7e0ea !important;
    color: #9ca3af !important; border-radius: 6px !important;
}

/* SLIDER */
[data-testid="stSlider"] [data-baseweb="slider"] > div > div {
    background: #d7e0ea !important;
    height: 4px !important; border-radius: 4px !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] > div > div:nth-child(2) {
    background: linear-gradient(90deg, #0ea5e9, #14b8a6) !important;
}
[data-testid="stSlider"] [role="slider"] {
    background: #0ea5e9 !important;
    border: 3px solid #ffffff !important;
    box-shadow: 0 0 0 2px #0ea5e9, 0 2px 8px rgba(14,165,233,0.28) !important;
    width: 18px !important; height: 18px !important;
}
[data-testid="stSlider"] [data-testid="stThumbValue"] {
    color: #0ea5e9 !important;
    font-family: 'Manrope', sans-serif !important;
    font-size: 12px !important; font-weight: 600 !important;
    background: transparent !important;
}
[data-testid="stSlider"] [data-testid="stTickBar"] > div {
    color: #9ca3af !important;
    font-size: 10px !important;
}

/* RADIO */
[data-testid="stRadio"] > div {
    display: flex !important; flex-direction: row !important; gap: 8px !important;
}
[data-testid="stRadio"] label {
    flex: 1 !important; padding: 9px 14px !important;
    background: rgba(255,255,255,0.92) !important;
    border: 1px solid #d7e0ea !important;
    border-radius: 14px !important; cursor: pointer !important;
    display: flex !important; align-items: center !important;
    gap: 8px !important; transition: all 0.15s !important;
}
[data-testid="stRadio"] label:hover { border-color: #0ea5e9 !important; }
[data-testid="stRadio"] label span:last-child {
    font-family: 'Manrope', sans-serif !important;
    font-size: 14px !important; font-weight: 400 !important;
    color: #0f172a !important;
    letter-spacing: 0 !important; text-transform: none !important;
}
[data-baseweb="radio"] > div {
    background: transparent !important;
    border: 2px solid #d1d5db !important;
    width: 14px !important; height: 14px !important;
}
[data-baseweb="radio"][aria-checked="true"] > div {
    background: #0ea5e9 !important; border-color: #0ea5e9 !important;
}

/* BUTTON */
[data-testid="stButton"] > button {
    width: 100% !important; padding: 14px !important;
    background: linear-gradient(135deg, #0f172a 0%, #0ea5e9 55%, #14b8a6 100%) !important; color: #ffffff !important;
    font-family: 'Manrope', sans-serif !important;
    font-size: 14px !important; font-weight: 600 !important;
    letter-spacing: 0 !important; text-transform: none !important;
    border: none !important; border-radius: 14px !important;
    cursor: pointer !important; margin-top: 24px !important;
    transition: all 0.15s ease !important;
}
[data-testid="stButton"] > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 10px 24px rgba(15,23,42,0.16) !important;
}

[data-testid="column"] { padding: 0 8px !important; }
[data-testid="column"]:first-child { padding-left: 0 !important; }
[data-testid="column"]:last-child  { padding-right: 0 !important; }

.glass-card {
    background: rgba(255,255,255,0.82);
    backdrop-filter: blur(18px);
    border: 1px solid rgba(148,163,184,0.18);
    box-shadow: 0 18px 45px rgba(15,23,42,0.06);
}
</style>
""", unsafe_allow_html=True)


# ══ NAV ═══════════════════════════════════════
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center;
                        padding:0 48px; height:64px; background:rgba(255,255,255,0.74);
                        border-bottom:1px solid rgba(148,163,184,0.18); backdrop-filter: blur(16px);">
  <div style="display:flex; align-items:center; gap:10px;">
        <div style="width:32px; height:32px; background:linear-gradient(135deg, #0ea5e9, #14b8a6); border-radius:10px;
                display:flex; align-items:center; justify-content:center; font-size:15px;">
      🏦
    </div>
    <div>
            <div style="font-size:16px; font-weight:800; color:#0f172a; letter-spacing:-0.02em;">
                Apex<span style="color:#0ea5e9;">Pulse</span>
      </div>
            <div style="font-size:11px; color:#64748b; margin-top:-1px;">
                Customer retention studio
      </div>
    </div>
  </div>
  <div style="display:flex; align-items:center; gap:6px; padding:6px 14px;
                            background:rgba(236,253,245,0.95); border:1px solid #bbf7d0; border-radius:999px;">
        <span style="width:7px; height:7px; background:#10b981; border-radius:50%;
                 display:inline-block;"></span>
        <span style="font-size:12px; font-weight:600; color:#047857;">Model Ready</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ══ HERO ══════════════════════════════════════
st.markdown("""
<div style="background:linear-gradient(135deg, #0f172a 0%, #0b3b61 52%, #0f766e 100%); padding:44px 48px 40px;">
    <div style="font-size:12px; font-weight:600; color:#a5f3fc;
                            margin-bottom:12px; letter-spacing:1px; text-transform:uppercase;">
        Client retention intelligence
  </div>
    <div style="font-size:clamp(30px,3.5vw,48px); font-weight:800;
                            color:#ffffff; line-height:1.1; margin-bottom:12px; letter-spacing:-0.03em;">
        Spot churn signals early<br>
        <span style="color:#67e8f9;">and act with confidence.</span>
    </div>
    <div style="max-width:720px; font-size:15px; line-height:1.7; color:#dbeafe;">
        A polished banking risk dashboard for comparing customer profiles, estimating churn probability, and suggesting the next best action.
  </div>
</div>
""", unsafe_allow_html=True)


# ══ STATS ROW ═════════════════════════════════
st.markdown("<div style='background:#1e3a8a; padding:0 48px;'>", unsafe_allow_html=True)
sc1, sc2, sc3, sc4 = st.columns(4)
stats = [
    (sc1, "10,000", "Profiles analysed",  "Training dataset size",   False),
    (sc2, "86.6%",  "Model accuracy",     "Random Forest",           True),
    (sc3, "3",      "Models compared",    "LR · DT · RF",            False),
    (sc4, "~20%",   "Typical churn rate",  "Industry baseline",       False),
]
for col, num, label, sub, hi in stats:
    col.markdown(
        '<div style="padding:20px 0 24px; border-right:1px solid rgba(255,255,255,0.08);">'
        '<div style="font-size:30px; font-weight:800; color:' + ('#67e8f9' if hi else '#c4b5fd') + '; margin-bottom:6px;">' + num + '</div>'
        '<div style="font-size:13px; font-weight:600; color:#f8fafc; margin-bottom:2px;">' + label + '</div>'
        '<div style="font-size:11px; color:#bfdbfe;">' + sub + '</div>'
        '</div>',
        unsafe_allow_html=True
    )
st.markdown("</div>", unsafe_allow_html=True)


# ══ MAIN BODY ═════════════════════════════════
st.markdown("<div style='padding:36px 48px; background:#f8f9fa;'>", unsafe_allow_html=True)
left, right = st.columns([1, 1], gap="large")


# ─── LEFT ─────────────────────────────────────
with left:
    st.markdown(
        '<div style="font-size:13px; font-weight:700; color:#0ea5e9;'
        'padding-bottom:10px; border-bottom:2px solid #0ea5e9; margin-bottom:4px; letter-spacing:0.02em;">'
        'Step 1 · Enter customer details</div>',
        unsafe_allow_html=True
    )

    def section(icon, title):
        st.markdown(
            '<div style="display:flex; align-items:center; gap:8px;'
            'margin-top:20px; margin-bottom:10px;">'
            '<span style="font-size:14px;">' + icon + '</span>'
            '<span style="font-size:12px; font-weight:700; color:#334155; text-transform:uppercase; letter-spacing:0.04em;">' + title + '</span>'
            '<div style="flex:1; height:1px; background:linear-gradient(90deg, rgba(148,163,184,0.45), transparent); margin-left:4px;"></div>'
            '</div>',
            unsafe_allow_html=True
        )

    section("", "Personal information")
    c1, c2 = st.columns(2)
    with c1: geography = st.selectbox("Country", le_geo.classes_)
    with c2: gender    = st.selectbox("Gender",  le_gen.classes_)

    c3, c4 = st.columns(2)
    with c3: age    = st.slider("Age",            18, 92, 38)
    with c4: tenure = st.slider("Tenure (Years)", 0,  10, 5)

    section("", "Financial information")
    c5, c6 = st.columns(2)
    with c5:
        credit_score = st.slider("Credit Score", 300, 850, 650)
        balance      = st.number_input("Account Balance ($)", 0.0, value=76000.0, step=500.0)
    with c6:
        num_products     = st.selectbox("Number of Products", [1, 2, 3, 4])
        estimated_salary = st.number_input("Annual Salary ($)", 0.0, value=85000.0, step=500.0)

    section("", "Account details")
    c7, c8 = st.columns(2)
    with c7: has_cr_card = st.radio("Has Credit Card?",  ["Yes", "No"], horizontal=True)
    with c8: is_active   = st.radio("Active Member?",    ["Yes", "No"], horizontal=True)

    predict = st.button("Generate risk forecast →", use_container_width=True)
    st.markdown("<div style='height:32px;'></div>", unsafe_allow_html=True)


# ─── RIGHT ────────────────────────────────────
with right:
    st.markdown(
        '<div style="font-size:13px; font-weight:700; color:#0ea5e9;'
        'padding-bottom:10px; border-bottom:2px solid #0ea5e9; margin-bottom:24px; letter-spacing:0.02em;">'
        'Step 2 · View prediction result</div>',
        unsafe_allow_html=True
    )

    if not predict:
        st.markdown("""
                <div class="glass-card" style="border-radius:18px; padding:52px 32px; text-align:center; margin-bottom:16px;">
          <div style="font-size:36px; margin-bottom:12px; opacity:0.3;">🏦</div>
          <div style="font-size:16px; font-weight:600; color:#374151; margin-bottom:8px;">
                        Waiting for inputs
          </div>
          <div style="font-size:13px; color:#9ca3af; line-height:1.6;">
                        Enter the customer profile on the left<br>
                        and generate the forecast here.
          </div>
        </div>""", unsafe_allow_html=True)

        # Quick facts
        st.markdown(
            '<div style="font-size:13px; font-weight:700; color:#334155;'
            'margin-bottom:12px;">Key signals from training</div>',
            unsafe_allow_html=True
        )
        facts = [
            ("", "Germany has the highest churn rate among all 3 countries."),
            ("", "Customers aged 40–60 are most likely to leave the bank."),
            ("", "Customers with only 1 product churn significantly more."),
            ("", "Inactive members are 3x more likely to churn."),
        ]
        for icon, text in facts:
            st.markdown(
                '<div style="display:flex; align-items:flex-start; gap:10px;'
                'padding:10px 14px; background:rgba(255,255,255,0.92); border:1px solid #d7e0ea;'
                'border-radius:14px; margin-bottom:8px; box-shadow:0 10px 25px rgba(15,23,42,0.04);">'
                '<span style="font-size:16px;">' + icon + '</span>'
                '<span style="font-size:13px; color:#334155; line-height:1.5;">' + text + '</span>'
                '</div>',
                unsafe_allow_html=True
            )

    else:
        geo_enc = le_geo.transform([geography])[0]
        gen_enc = le_gen.transform([gender])[0]
        cr_card = 1 if has_cr_card == "Yes" else 0
        active  = 1 if is_active   == "Yes" else 0

        inp = pd.DataFrame([[
            credit_score, geo_enc, gen_enc, age, tenure,
            balance, num_products, cr_card, active, estimated_salary
        ]], columns=feature_names)

        prob       = model.predict_proba(scaler.transform(inp))[0][1]
        prediction = model.predict(scaler.transform(inp))[0]
        pct        = int(prob * 100)
        stay       = 100 - pct

        if prediction == 1:
            r_bg    = "#fff1f2"
            r_bdr   = "#fda4af"
            r_top   = "#e11d48"
            r_color = "#be123c"
            r_icon  = ""
            r_label = "Elevated churn risk"
            r_sub   = "This customer is likely to leave. Intervene early."
            actions = [
                ("", "Reach out quickly",    "Assign a relationship manager to contact within 24 hours."),
                ("", "Offer a better rate",  "Present a personalised rate revision or fee waiver."),
                ("", "Bundle more products", "Offer a second product to improve stickiness."),
                ("", "Ask for feedback",     "Schedule a satisfaction review call to understand issues."),
            ]
        else:
            r_bg    = "#ecfdf5"
            r_bdr   = "#86efac"
            r_top   = "#059669"
            r_color = "#047857"
            r_icon  = ""
            r_label = "Low churn risk"
            r_sub   = "This customer is stable. Focus on growth."
            actions = [
                ("", "Upsell a product",    "Identify a premium product they'd benefit from."),
                ("", "Upgrade their tier",  "Enrol them in a loyalty or rewards programme."),
                ("", "Offer wealth advice",  "Suggest an investment or wealth management session."),
                ("", "Check satisfaction",  "Do a quick NPS or feedback call this quarter."),
            ]

        # RESULT CARD
        st.markdown(
            '<div style="background:' + r_bg + '; border:1px solid ' + r_bdr + ';'
            'border-left:4px solid ' + r_top + '; border-radius:18px;'
            'padding:24px; margin-bottom:16px; box-shadow:0 16px 36px rgba(15,23,42,0.05);">'
            '<div style="display:flex; justify-content:space-between; align-items:center;">'
            '<div>'
            '<div style="font-size:13px; color:' + r_color + '; font-weight:700; margin-bottom:6px; text-transform:uppercase; letter-spacing:0.03em;">'
            + r_icon + ' &nbsp;' + r_label + '</div>'
            '<div style="font-size:22px; font-weight:800; color:#0f172a; margin-bottom:6px; letter-spacing:-0.02em;">'
            + str(pct) + '% Churn Probability</div>'
            '<div style="font-size:13px; color:#475569;">' + r_sub + '</div>'
            '</div></div>'
            '<div style="margin-top:16px;">'
            '<div style="height:8px; background:#e2e8f0; border-radius:999px; overflow:hidden;">'
            '<div style="height:8px; width:' + str(pct) + '%; background:linear-gradient(90deg, ' + r_top + ', ' + r_color + '); border-radius:999px;"></div>'
            '</div>'
            '<div style="display:flex; justify-content:space-between; margin-top:4px;">'
            '<span style="font-size:11px; color:#94a3b8;">0% — stable</span>'
            '<span style="font-size:11px; color:#94a3b8;">100% — at risk</span>'
            '</div></div></div>',
            unsafe_allow_html=True
        )

        # METRICS
        mx1, mx2, mx3, mx4 = st.columns(4)
        for col, val, lbl, clr in [
            (mx1, str(pct) + "%",  "Churn Risk",  r_color),
            (mx2, str(stay) + "%", "Will Stay",   "#16a34a"),
            (mx3, "RF",            "Model used",  "#0ea5e9"),
            (mx4, "86.6%",         "Accuracy",    "#0ea5e9"),
        ]:
            col.markdown(
                '<div class="glass-card" style="border-radius:14px; padding:14px 10px; text-align:center; margin-bottom:14px;">'
                '<div style="font-size:20px; font-weight:800; color:' + clr + '; margin-bottom:4px;">' + val + '</div>'
                '<div style="font-size:11px; color:#64748b;">' + lbl + '</div>'
                '</div>',
                unsafe_allow_html=True
            )

        # SNAPSHOT + ACTIONS
        snap_col, act_col = st.columns(2, gap="medium")

        with snap_col:
            rows = [
                ("Country",      geography,                False),
                ("Gender",       gender,                   False),
                ("Age",          str(age) + " years",      False),
                ("Tenure",       str(tenure) + " years",   False),
                ("Credit Score", str(credit_score),        False),
                ("Balance",      "$" + f"{balance:,.0f}",  False),
                ("Products",     str(num_products),        False),
                ("Credit Card",  has_cr_card,              False),
                ("Active",       is_active,                False),
                ("Result",       r_label,                  True),
            ]
            table_html = build_table(rows, r_color)
            st.markdown(
                '<div class="glass-card" style="border-radius:18px; padding:16px;">'
                '<div style="font-size:12px; font-weight:700; color:#334155;'
                'margin-bottom:12px; text-transform:uppercase; letter-spacing:0.04em;">Customer summary</div>'
                + table_html + '</div>',
                unsafe_allow_html=True
            )

        with act_col:
            acts_html = ""
            for em, t, d in actions:
                acts_html += (
                    '<div style="display:flex; gap:10px; padding:10px 0;'
                    'border-bottom:1px solid #f3f4f6; align-items:flex-start;">'
                    '<span style="font-size:18px; flex-shrink:0;">' + em + '</span>'
                    '<div>'
                    '<div style="font-size:13px; font-weight:600; color:#1a1a1a;'
                    'margin-bottom:2px;">' + t + '</div>'
                    '<div style="font-size:12px; color:#6b7280; line-height:1.5;">' + d + '</div>'
                    '</div></div>'
                )
            st.markdown(
                '<div class="glass-card" style="border-radius:18px; padding:16px;">'
                '<div style="font-size:12px; font-weight:700; color:#334155;'
                'margin-bottom:4px; text-transform:uppercase; letter-spacing:0.04em;">Recommended actions</div>'
                + acts_html + '</div>',
                unsafe_allow_html=True
            )

        st.markdown("<div style='height:32px;'></div>", unsafe_allow_html=True)

st.markdown(
    '<div style="padding:0 48px 28px; color:#64748b; font-size:12px;">'
    'ApexPulse retention studio · Streamlit dashboard for bank customer churn scoring.'</div>',
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)