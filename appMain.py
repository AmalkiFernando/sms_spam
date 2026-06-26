import streamlit as st
import joblib
import re
import string

st.set_page_config(
    page_title="SpamShield — AI Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

/* ─── BASE ─── */
.stApp {
    background: linear-gradient(145deg, #0f1f0f 0%, #132213 40%, #0a1a14 100%);
    font-family: 'Plus Jakarta Sans', sans-serif;
    min-height: 100vh;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2rem 3rem 3rem !important;
    max-width: 1080px !important;
}

/* ─── HERO ─── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
}
.hero-eyebrow {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.35em;
    color: #4ade80;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.hero-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: clamp(2.6rem, 5vw, 3.8rem);
    font-weight: 800;
    color: #f0faf2;
    line-height: 1.1;
    margin-bottom: 0.6rem;
}
.hero-title .accent { color: #4ade80; }
.hero-subtitle {
    font-size: 1rem;
    color: #6aaf7a;
    font-weight: 400;
}

/* ─── STATUS PILLS ─── */
.status-bar {
    display: flex;
    justify-content: center;
    gap: 1rem;
    flex-wrap: wrap;
    margin: 1.25rem 0 2rem;
}
.pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(74,222,128,0.08);
    border: 1px solid rgba(74,222,128,0.2);
    border-radius: 100px;
    padding: 4px 12px;
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.12em;
    color: #86efac;
    text-transform: uppercase;
}
.pill-dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: #4ade80;
    box-shadow: 0 0 6px #4ade80;
    animation: blink 2.2s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.25} }

/* ─── CARDS ─── */
.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(74,222,128,0.15);
    border-radius: 18px;
    padding: 1.75rem;
    margin-bottom: 1.25rem;
}
.card-top-line {
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(74,222,128,0.5), transparent);
    border-radius: 2px;
    margin-bottom: 1.25rem;
}
.card-label {
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.3em;
    color: #4ade80;
    text-transform: uppercase;
    margin-bottom: 0.85rem;
    opacity: 0.85;
}

/* ─── TEXTAREA ─── */
.stTextArea > div > div > textarea {
    background: rgba(10, 30, 15, 0.85) !important;
    border: 1.5px solid rgba(74,222,128,0.25) !important;
    border-radius: 12px !important;
    color: #e2f5e6 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.95rem !important;
    line-height: 1.65 !important;
    padding: 1rem 1.1rem !important;
    caret-color: #4ade80 !important;
    resize: vertical !important;
}
.stTextArea > div > div > textarea:focus {
    border-color: #4ade80 !important;
    box-shadow: 0 0 0 3px rgba(74,222,128,0.1) !important;
    outline: none !important;
}
.stTextArea > div > div > textarea::placeholder {
    color: rgba(106,175,122,0.45) !important;
}
.stTextArea label { display: none !important; }

/* ─── BUTTON ─── */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #16a34a, #22c55e) !important;
    border: none !important;
    color: #ffffff !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    letter-spacing: 0.04em !important;
    border-radius: 12px !important;
    height: 54px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(34,197,94,0.3) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #15803d, #16a34a) !important;
    box-shadow: 0 6px 28px rgba(34,197,94,0.45) !important;
    transform: translateY(-2px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ─── RESULT CARDS ─── */
.result-spam {
    background: rgba(239,68,68,0.08);
    border: 1.5px solid rgba(239,68,68,0.35);
    border-radius: 16px;
    padding: 1.75rem 1.75rem 1.5rem;
    margin-top: 1.25rem;
    position: relative;
    overflow: hidden;
}
.result-ham {
    background: rgba(74,222,128,0.07);
    border: 1.5px solid rgba(74,222,128,0.35);
    border-radius: 16px;
    padding: 1.75rem 1.75rem 1.5rem;
    margin-top: 1.25rem;
    position: relative;
    overflow: hidden;
}

.verdict-icon {
    font-size: 2.2rem;
    margin-bottom: 0.4rem;
    line-height: 1;
}
.verdict-label {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 800;
    font-size: clamp(1.4rem, 3vw, 2rem);
    margin-bottom: 0.25rem;
    line-height: 1.1;
}
.result-spam .verdict-label { color: #fca5a5; }
.result-ham  .verdict-label { color: #86efac; }

.verdict-conf {
    font-size: 0.85rem;
    font-weight: 500;
    margin-bottom: 1.5rem;
}
.result-spam .verdict-conf { color: #f87171; }
.result-ham  .verdict-conf { color: #4ade80; }

/* ─── BARS ─── */
.bar-wrap { margin-bottom: 0.65rem; }
.bar-meta {
    display: flex;
    justify-content: space-between;
    margin-bottom: 4px;
}
.bar-name {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #9ca3af;
}
.bar-pct {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: #d1fae5;
}
.bar-track {
    height: 7px;
    background: rgba(255,255,255,0.06);
    border-radius: 6px;
    overflow: hidden;
}
.bar-fill-spam {
    height: 100%;
    border-radius: 6px;
    background: linear-gradient(90deg, #7f1d1d, #ef4444);
}
.bar-fill-ham {
    height: 100%;
    border-radius: 6px;
    background: linear-gradient(90deg, #14532d, #4ade80);
}

/* ─── INFO PANEL ─── */
.info-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(74,222,128,0.13);
    border-radius: 18px;
    padding: 1.5rem;
}
.info-title {
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.3em;
    color: #4ade80;
    text-transform: uppercase;
    margin-bottom: 1.25rem;
    opacity: 0.8;
}
.spec-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.6rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.spec-row:last-child { border-bottom: none; }
.spec-key {
    font-size: 0.8rem;
    color: #6aaf7a;
    font-weight: 400;
}
.spec-val {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: #d1fae5;
    text-align: right;
}
.active-badge {
    background: rgba(74,222,128,0.15);
    border: 1px solid rgba(74,222,128,0.35);
    color: #4ade80;
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.1em;
    border-radius: 100px;
    padding: 2px 10px;
}

/* ─── FOOTER ─── */
.footer {
    text-align: center;
    margin-top: 2.5rem;
    padding-top: 1.25rem;
    border-top: 1px solid rgba(74,222,128,0.1);
}
.footer-text {
    font-size: 0.78rem;
    color: #3d6b4a;
    letter-spacing: 0.05em;
}

/* ─── OVERRIDES ─── */
div[data-testid="stVerticalBlock"] { background: transparent !important; backdrop-filter: none !important; }
div[data-testid="column"] { background: transparent !important; }
p, label, div { color: inherit; }
h1,h2,h3,h4 { color: #f0faf2 !important; }
</style>
""", unsafe_allow_html=True)

# Load model
model = joblib.load("spam_classifier.pkl")
vectorizer = joblib.load("count_vectorizer.pkl")

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.strip()

# ── Hero ──────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">🛡️ &nbsp; AI-Powered Message Analysis</div>
  <div class="hero-title">Spam<span class="accent">Shield</span></div>
  <div class="hero-subtitle">Detect spam instantly with machine learning</div>
</div>
<div class="status-bar">
  <span class="pill"><span class="pill-dot"></span>Model Online</span>
  <span class="pill"><span class="pill-dot"></span>Logistic Regression</span>
  <span class="pill"><span class="pill-dot"></span>CountVectorizer</span>
</div>
""", unsafe_allow_html=True)

# ── Layout ────────────────────────────────────────────────
col_main, col_info = st.columns([2.2, 1], gap="large")

with col_info:
    st.markdown("""
    <div class="info-card">
      <div class="info-title">Model Info</div>
      <div class="spec-row">
        <span class="spec-key">Labels</span>
        <span class="spec-val">HAM &nbsp;/&nbsp; SPAM</span>
      </div>
      <div class="spec-row">
        <span class="spec-key">Status</span>
        <span class="active-badge">● Active</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_main:
    # Input card wrapper (label only — textarea rendered by Streamlit)
    
    
    message = st.text_area(
        "msg",
        height=200,
        placeholder="Paste or type your SMS or email message here…",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    clicked = st.button("🔍  Analyze Message")

    if clicked:
        if message.strip():
            cleaned = clean_text(message)
            vector = vectorizer.transform([cleaned])
            prediction = model.predict(vector)[0]
            probs = model.predict_proba(vector)[0]
            ham_prob  = probs[0] * 100
            spam_prob = probs[1] * 100

            if prediction == 1:
                st.markdown(f"""
                <div class="result-spam">
                  <div class="verdict-icon">🚨</div>
                  <div class="verdict-label">Spam Detected</div>
                  <div class="verdict-conf">Threat confidence: {spam_prob:.1f}%</div>
                  <div class="bar-wrap">
                    <div class="bar-meta">
                      <span class="bar-name">Spam</span>
                      <span class="bar-pct">{spam_prob:.1f}%</span>
                    </div>
                    <div class="bar-track"><div class="bar-fill-spam" style="width:{spam_prob:.1f}%"></div></div>
                  </div>
                  <div class="bar-wrap">
                    <div class="bar-meta">
                      <span class="bar-name">Ham</span>
                      <span class="bar-pct">{ham_prob:.1f}%</span>
                    </div>
                    <div class="bar-track"><div class="bar-fill-ham" style="width:{ham_prob:.1f}%"></div></div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-ham">
                  <div class="verdict-icon">✅</div>
                  <div class="verdict-label">Legitimate Message</div>
                  <div class="verdict-conf">Clear confidence: {ham_prob:.1f}%</div>
                  <div class="bar-wrap">
                    <div class="bar-meta">
                      <span class="bar-name">Ham</span>
                      <span class="bar-pct">{ham_prob:.1f}%</span>
                    </div>
                    <div class="bar-track"><div class="bar-fill-ham" style="width:{ham_prob:.1f}%"></div></div>
                  </div>
                  <div class="bar-wrap">
                    <div class="bar-meta">
                      <span class="bar-name">Spam</span>
                      <span class="bar-pct">{spam_prob:.1f}%</span>
                    </div>
                    <div class="bar-track"><div class="bar-fill-spam" style="width:{spam_prob:.1f}%"></div></div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="result-ham" style="border-color:rgba(255,255,255,0.1); background:rgba(255,255,255,0.02);">
              <div class="verdict-icon">💬</div>
              <div class="verdict-label" style="color:#6aaf7a; font-size:1.2rem;">No message entered</div>
              <div class="verdict-conf" style="color:#3d6b4a;">Please type or paste a message above and try again.</div>
            </div>
            """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <div class="footer-text">SpamShield · Built by Amalki Fernando</div>
</div>
""", unsafe_allow_html=True)