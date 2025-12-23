import streamlit as st
import json
import statistics
import pandas as pd
import hashlib

# --- PAGE CONFIG ---
st.set_page_config(page_title="ALIVE Portal", page_icon="🧬", layout="centered")

# --- 1. CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .status-header {
        font-family: 'Courier New', Courier, monospace;
        color: #00ff00;
        font-size: 26px;
        font-weight: bold;
        letter-spacing: 2px;
    }
    .pulse {
        display: inline-block;
        width: 15px;
        height: 15px;
        background: #00ff00;
        border-radius: 50%;
        box-shadow: 0 0 10px rgba(0, 255, 0, 1);
        animation: pulse-green 2s infinite;
        margin-right: 15px;
        vertical-align: middle;
    }
    @keyframes pulse-green {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 0, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(0, 255, 0, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 0, 0); }
    }
    [data-testid="stFileUploader"] {
        border: 2px solid #000000;
        background-color: #A9A9A9;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HEADER ---
st.title("🧬 ALIVE PORTAL")
st.write("### BIOMETRIC & CONTENT VERIFICATION")
st.info("Step 1: Upload the JSON receipt. Step 2: Paste the text to verify.")

# --- 3. INPUTS ---
col1, col2 = st.columns([1, 1])

with col1:
    uploaded_file = st.file_uploader("Upload rhythm.json", type=["json"])

with col2:
    pasted_text = st.text_area("Paste the article/text here:", height=150)

# --- 4. VERIFICATION LOGIC ---
if uploaded_file is not None and pasted_text:
    try:
        # Load JSON data
        raw_data = json.load(uploaded_file)
        
        # In the new version, data is in 'jitter_data' key
        jitter = raw_data.get("jitter_data", [])
        saved_hash = raw_data.get("content_hash", "")
        
        # Calculate Hash of the pasted text
        current_hash = hashlib.sha256(pasted_text.strip().encode('utf-8')).hexdigest()
        
        # --- PHASE A: CONTENT INTEGRITY CHECK ---
        st.divider()
        if current_hash == saved_hash:
            st.success("🔒 CONTENT INTEGRITY VERIFIED: This text matches the recorded session exactly.")
            hash_match = True
        else:
            st.error("🚨 TAMPER ALERT: The pasted text does not match the digital fingerprint in this receipt.")
            st.warning(f"Expected Hash: {saved_hash[:10]}... | Current Hash: {current_hash[:10]}...")
            hash_match = False

        # --- PHASE B: BIOMETRIC CHECK ---
        if len(jitter) > 10:
            variation = statistics.stdev(jitter)
            score = min(100, int(variation * 500)) 
            
            if score > 70 and hash_match:
                st.markdown(f'<div class="status-header"><div class="pulse"></div> STATUS: VERIFIED HUMAN</div>', unsafe_allow_html=True)
                st.metric(label="Humanity Confidence", value=f"{score}%")
                
                st.write("### 🧬 Rhythmic Signature")
                chart_data = pd.DataFrame(jitter[:100], columns=["Jitter"])
                st.line_chart(chart_data, color="#00ff00")

                # --- NEW MULTI-PLATFORM BADGE GENERATOR ---
                st.write("### 🛡️ Share Your Verification")
                st.write("Choose the format that fits your platform.")
                
                short_hash = saved_hash[:6]
                badge_id = f"{score}-H-{short_hash}-2025"
                portal_url = "https://alive-prototype.streamlit.app/"
                
                tab1, tab2 = st.tabs(["🌐 Web Badge (HTML)", "📱 Social Media (Text)"])
                
                with tab1:
                    st.write("Copy this into the HTML of your blog or website:")
                    badge_code = f"""<div style="padding:15px; border:2px solid #00ff00; border-radius:10px; background-color:#1a1c24; text-align:center;">
    <a href="{portal_url}" style="color:#00ff00; text-decoration:none; font-family:monospace; font-weight:bold;">
        [a] ALIVE CERTIFIED HUMAN | ID: {badge_id}
    </a>
</div>"""
                    st.code(badge_code, language="html")

                with tab2:
                    st.write("Copy this into your social media post description:")
                    social_text = f"🧬 [a] ALIVE Verified Human\nID: {badge_id}\nVerify at: {portal_url}"
                    st.code(social_text, language="text")
                
                st.balloons()
            elif hash_match:
                st.warning("Content matches, but biological jitter is too low. Possible AI-assisted input.")
        else:
            st.info("Biometric data stream is too short for a confidence score.")

    except Exception as e:
        st.error(f"Error parsing verification file: {e}")
else:
    st.write("📡 Waiting for both Receipt and Content for full verification...")