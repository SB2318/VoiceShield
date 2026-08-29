import streamlit as st
import time
import random
import hashlib
from datetime import datetime

# Configure page
st.set_page_config(page_title="VoiceShield PoC", page_icon="🛡️", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .main-header {
        font-size: 40px;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
    }
    .sub-header {
        font-size: 20px;
        color: #4B5563;
        text-align: center;
        margin-bottom: 30px;
    }
    .alert-box-fake {
        padding: 20px;
        background-color: #FEE2E2;
        border-left: 5px solid #EF4444;
        color: #991B1B;
        border-radius: 5px;
        font-weight: bold;
        font-size: 24px;
        text-align: center;
        margin: 20px 0;
    }
    .alert-box-real {
        padding: 20px;
        background-color: #D1FAE5;
        border-left: 5px solid #10B981;
        color: #065F46;
        border-radius: 5px;
        font-weight: bold;
        font-size: 24px;
        text-align: center;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🛡️ VoiceShield</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Real-Time Detection of Voice Cloning (SIH26104)</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Configuration")
st.sidebar.info("Use this panel to control the outcome of the demo for the video pitch.")
scenario = st.sidebar.selectbox(
    "Select Scenario for Demo",
    ["Scenario A: Authentic Voice (Real)", "Scenario B: Deepfake Voice (Spoofed)", "Scenario C: High-Risk Unverified (Trigger Liveness)"]
)

# Main App
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 🎙️ Call Audio Input")
    st.info("In production, this intercepts WebRTC/SIP streams. For this PoC, upload an audio clip to simulate the stream.")
    
    audio_file = st.file_uploader("Upload Audio Chunk (WAV/MP3)", type=['wav', 'mp3'])
    
    analyze_btn = st.button("Run Multi-View Analysis 🚀", use_container_width=True)

if analyze_btn:
    with col2:
        st.markdown("### 🧠 Analysis Engine Running...")
        
        # Mock Processing Steps
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        steps = [
            "Ingestion & Preprocessing (VAD, Chunking)...",
            "Extracting Raw Waveform Features...",
            "Generating LFCC / CQT Spectrograms...",
            "Extracting Self-Supervised (SSL) Embeddings...",
            "Attention-Based Fusion & Cross-Branch Gate Check..."
        ]
        
        for i, step in enumerate(steps):
            status_text.text(step)
            progress_bar.progress((i + 1) * 20)
            time.sleep(0.8) # Artificial delay for video effect
            
        status_text.empty()
        progress_bar.empty()
        
        st.markdown("---")
        st.markdown("### 📊 Detection Results")
        
        # Scenario Logic
        if "Authentic" in scenario:
            st.markdown('<div class="alert-box-real">✅ PASS: Authentic Human Voice</div>', unsafe_allow_html=True)
            risk_score = random.uniform(1.2, 5.8)
            
            st.write(f"**Spoof Probability Score:** {risk_score:.2f}% (Real)")
            
            # XAI Explanation
            with st.expander("🔍 XAI Explainability Data", expanded=True):
                st.write("- **RawNet2 Branch:** Natural breath patterns detected.")
                st.write("- **Spectrogram Branch:** Harmonics consistent with human vocal tract.")
                st.write("- **SSL Branch:** Prosody matches baseline human speech.")
                
            # Blockchain Audit
            with st.expander("🔗 Blockchain Audit Trail"):
                tx_hash = hashlib.sha256(f"real_{time.time()}".encode()).hexdigest()
                st.code(f"Timestamp: {datetime.now()}\nStatus: Verified\nLedger Hash: {tx_hash}\nAction: Allow Call", language="text")

        elif "Deepfake" in scenario:
            st.markdown('<div class="alert-box-fake">🚨 ALERT: Synthetic Voice Cloned Detected!</div>', unsafe_allow_html=True)
            risk_score = random.uniform(92.5, 98.9)
            
            st.write(f"**Spoof Probability Score:** {risk_score:.2f}%")
            
            # XAI Explanation
            with st.expander("🔍 XAI Explainability Data", expanded=True):
                st.write("- **RawNet2 Branch:** Missing natural breathing pauses.")
                st.write("- **Spectrogram Branch:** Unnatural harmonic structure in 2–4 kHz band.")
                st.write("- **SSL Branch:** Unnaturally steady pitch, phasing anomalies detected.")
                
            # Action Orchestrator
            st.error("🛡️ Action Orchestrator: Call Muted. Alert Sent to Bank Fraud SOC.")
            
            # Blockchain Audit
            with st.expander("🔗 Blockchain Audit Trail"):
                tx_hash = hashlib.sha256(f"fake_{time.time()}".encode()).hexdigest()
                st.code(f"Timestamp: {datetime.now()}\nStatus: BLOCKED\nLedger Hash: {tx_hash}\nAction: Auto-Freeze Triggered", language="text")

        elif "High-Risk" in scenario:
            st.warning("⚠️ RISK ROUTER: Medium Confidence / Speaker Mismatch")
            st.write("**Decision:** Escalating to Audio-Domain Liveness Challenge")
            
            st.markdown("### 🗣️ GOTCHA Liveness Challenge Triggered")
            challenge_phrase = "Please repeat immediately: 'Blue elephants jump quickly'"
            st.info(f"**System Prompt to Caller:** {challenge_phrase}")
            
            st.write("Awaiting user response...")
            time.sleep(2.5)
            
            st.error("❌ Challenge Failed: Prosody timing inconsistent with live reading. Action: Call Dropped.")
