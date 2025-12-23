import streamlit as st
import json
import statistics

# --- 1. BRANDING & STYLE ---
st.set_page_config(page_title="Alive Portal", page_icon="🟢")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .status-header {
        color: #ffffff !important;
        font-family: 'Courier New', Courier, monospace;
        letter-spacing: 2px;
        font-weight: bold;
        display: flex;
        align-items: center;
        font-size: 24px;
        margin-bottom: 20px;
    }
    .pulse {
        width: 18px; height: 18px;
        background: #00ff00;
        border-radius: 50%;
        box-shadow: 0 0 0 rgba(0, 255, 0, 0.4);
        animation: pulse 2s infinite;
        display: inline-block;
        margin-right: 15px;
    }
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 0, 0.8); }
        70% { transform: scale(1); box-shadow: 0 0 0 12px rgba(0, 255, 0, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 0, 0); }
    }
    .badge-box {
        background-color: #1a1c24;
        padding: 20px;
        border: 2px solid #00ff00;
        border-radius: 5px;
        color: #00ff00;
        font-family: monospace;
        text-align: center;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🟢 Alive (a.live)")
st.write("---")

uploaded_file = st.file_uploader("Upload Humanity Receipt", type="json")

if uploaded_file is not None:
    data = json.load(uploaded_file)
    
    if len(data) > 10:
        variation = statistics.stdev(data)
        score = min(100, int(variation * 500)) 
        
        if score > 70:
            st.markdown(f'<div class="status-header"><div class="pulse"></div> STATUS: VERIFIED HUMAN</div>', unsafe_allow_html=True)
            st.balloons()
            
            # --- THE BADGE GENERATOR ---
            st.write("### Your H-Mark is Ready")
            st.info("You have successfully proven your biological origin. Copy the badge below to your blog.")
            
            # This is the "Text Badge" they can copy
            badge_text = f" [a] ALIVE CERTIFIED | ID: {score}-H-2025 "
            
            st.markdown(f'<div class="badge-box">{badge_text}</div>', unsafe_allow_html=True)
            
            st.text_input("Copy this code to your website footer:", value=f"<span>{badge_text}</span>")
            
            st.download_button(
                label="Download Verified Certificate",
                data=json.dumps(data),
                file_name="Alive_Verified_Certificate.json",
                mime="application/json"
            )
        else:
            st.error("VERIFICATION FAILED: Rhythm too consistent (Possible AI)")
    else:
        st.warning("Data sample too small. Please record a longer writing session.")