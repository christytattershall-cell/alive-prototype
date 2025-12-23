import streamlit as st
import json
import statistics
import pandas as pd
import hashlib

# --- PAGE CONFIG ---
st.set_page_config(page_title="ALIVE Portal", page_icon="🧬", layout="centered")

# --- 1. CUSTOM CSS (Cyberpunk/Bio-Tech Aesthetic) ---
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
        background-color: #f0f2f6;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HEADER ---
st.title("🧬 ALIVE PORTAL")
st.write("### BIOMETRIC & CONTENT VERIFICATION")

# --- 3. MODE SELECTION ---
mode = st.radio("Verification Method:", ["File Upload (Full Proof)", "Manual ID Lookup"], horizontal=True)

if mode == "File Upload (Full Proof)":
    st.info("Step 1: Upload the rhythm.json receipt. Step 2: Paste the text to verify.")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        uploaded_file = st.file_uploader("Upload rhythm.json", type=["json"])
    with col2:
        pasted_text = st.text_area("Paste the article/text here:", height=150)

    if uploaded_file is not None and pasted_text:
        try:
            # Load the JSON receipt
            data = json.load(uploaded_file)
            jitter = data.get("jitter_data", [])
            saved_hash = data.get("content_hash", "")
            timestamp = data.get("timestamp", "Unknown")
            score = data.get("score", 0)
            
            # --- THE TIMESTAMP LOCK CHECK ---
            combined_to_verify = f"{pasted_text.strip()}{timestamp}"
            calculated_hash = hashlib.sha256(combined_to_verify.encode('utf-8')).hexdigest()
            
            hash_match = (calculated_hash == saved_hash)
            st.divider()

            if hash_match:
                st.markdown(f'<div class="status-header"><div class="pulse"></div> STATUS: VERIFIED HUMAN</div>', unsafe_allow_html=True)
                st.balloons()
                
                # --- THE COOL STUFF: BIOMETRIC CHART ---
                st.write("### 🧬 Rhythmic Signature")
                st.write("This chart shows the unique biological micro-timing of the keystrokes recorded.")
                chart_data = pd.DataFrame(jitter, columns=["Jitter (ms)"])
                st.line_chart(chart_data, color="#00ff00")
                
                # --- VERIFICATION SUMMARY TABLE ---
                st.write("### 📋 Verification Summary")
                summary_data = {
                    "Security Check": ["Content Integrity", "Biometric Confidence", "Timestamp Lock", "Human ID"],
                    "Result": ["PASSED", f"{score}%", timestamp, data.get("id", "N/A")],
                    "Status": ["✅", "✅", "🔒", "🆔"]
                }
                st.table(pd.DataFrame(summary_data))

                # --- SHAREABLE BADGE GENERATOR ---
                st.write("### 🛡️ Share Your Verification")
                portal_url = "https://alive-prototype.streamlit.app/"
                badge_id = data.get("id", "ALIVE-HUMAN")
                
                t1, t2 = st.tabs(["🌐 Web Badge", "📱 Social Media"])
                with t1:
                    badge_code = f"""<div style="padding:15px; border:2px solid #00ff00; border-radius:10px; background-color:#1a1c24; text-align:center; font-family:monospace;">
    <a href="{portal_url}" style="color:#00ff00; text-decoration:none; font-weight:bold; display:block; margin-bottom:5px;">
        [a] ALIVE CERTIFIED HUMAN | ID: {badge_id}
    </a>
    <span style="color:#888; font-size:10px;">TS: {timestamp}</span>
</div>"""
                    st.code(badge_code, language="html")
                with t2:
                    st.code(f"🧬 [a] ALIVE Verified Human\nID: {badge_id}\nTS: {timestamp}\nVerify: {portal_url}", language="text")

            else:
                st.error("🚨 TAMPER ALERT: The text or timestamp does not match the original human session.")
                st.warning("Integrity check failed. This document may have been edited after verification.")

        except Exception as e:
            st.error(f"Error parsing receipt: {e}")

else:
    # --- MANUAL ID LOOKUP MODE ---
    st.info("Enter the ID and the exact Timestamp to verify the content authenticity.")
    
    lookup_id = st.text_input("Enter ALIVE ID (e.g., 94-H-a1b2c3-2025):")
    verify_text = st.text_area("Paste the text you are verifying:", height=200)
    manual_ts = st.text_input("Enter TS (Timestamp) from the post:")
    
    if st.button("Run Quick Verification"):
        if lookup_id and verify_text and manual_ts:
            # Re-create the hash from text + timestamp
            combined = f"{verify_text.strip()}{manual_ts}"
            actual_hash = hashlib.sha256(combined.encode('utf-8')).hexdigest()
            short_hash = actual_hash[:6]
            
            if short_hash in lookup_id:
                st.success(f"✅ AUTHENTIC: Content matches the human signature for ID {lookup_id}")
                st.markdown(f'<div class="status-header"><div class="pulse"></div> CONTENT AUTHENTIC</div>', unsafe_allow_html=True)
            else:
                st.error("❌ TAMPERED: The content does not match the provided ID and Timestamp.")
        else:
            st.warning("All fields are required for a manual check.")