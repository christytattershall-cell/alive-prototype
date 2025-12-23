import streamlit as st
import json
import statistics
import pandas as pd
import hashlib
from datetime import datetime

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
    .cert-table {
        width: 100%;
        border-collapse: collapse;
        font-family: monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HEADER ---
st.title("🧬 ALIVE PORTAL")

# --- 3. MODE SELECTION ---
mode = st.radio("Select Verification Mode:", ["File Upload (Full Proof)", "ID Lookup (Quick Check)"], horizontal=True)

if mode == "File Upload (Full Proof)":
    st.info("Step 1: Upload the JSON receipt. Step 2: Paste the text to verify.")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        uploaded_file = st.file_uploader("Upload rhythm.json", type=["json"])
    with col2:
        pasted_text = st.text_area("Paste the article/text here:", height=150)

    if uploaded_file is not None and pasted_text:
        try:
            raw_data = json.load(uploaded_file)
            jitter = raw_data.get("jitter_data", [])
            saved_hash = raw_data.get("content_hash", "")
            timestamp = raw_data.get("timestamp", "Unknown")
            
            current_hash = hashlib.sha256(pasted_text.strip().encode('utf-8')).hexdigest()
            
            st.divider()
            
            # Checks
            hash_match = current_hash == saved_hash
            variation = statistics.stdev(jitter) if len(jitter) > 10 else 0
            score = min(100, int(variation * 500))
            human_verified = score > 70

            # --- VERDICT ---
            if hash_match and human_verified:
                st.markdown(f'<div class="status-header"><div class="pulse"></div> STATUS: VERIFIED HUMAN</div>', unsafe_allow_html=True)
                st.balloons()
            else:
                st.error("⚠️ VERIFICATION FAILED: Critical mismatch detected.")

            # --- VERIFICATION SUMMARY TABLE ---
            st.write("### 📋 Verification Summary")
            summary_data = {
                "Security Check": ["Content Integrity", "Biometric Jitter", "Fingerprint Match", "Timestamp"],
                "Result": [
                    "PASSED" if hash_match else "FAILED",
                    f"{score}% Confidence",
                    f"Match ({saved_hash[:6]})" if hash_match else "MISMATCH",
                    timestamp
                ],
                "Status": ["✅" if hash_match else "❌", "✅" if human_verified else "❌", "✅" if hash_match else "❌", "ℹ️"]
            }
            st.table(pd.DataFrame(summary_data))

            if human_verified and hash_match:
                # --- SHAREABLE BADGE ---
                st.write("### 🛡️ Share Your Verification")
                short_hash = saved_hash[:6]
                badge_id = f"{score}-H-{short_hash}-2025"
                portal_url = "https://alive-prototype.streamlit.app/"
                
                t1, t2 = st.tabs(["🌐 Web Badge", "📱 Social Media"])
                with t1:
                    badge_code = f'<div style="padding:15px; border:2px solid #00ff00; border-radius:10px; background-color:#1a1c24; text-align:center;"><a href="{portal_url}" style="color:#00ff00; text-decoration:none; font-family:monospace; font-weight:bold;">[a] ALIVE CERTIFIED HUMAN | ID: {badge_id}</a></div>'
                    st.code(badge_code, language="html")
                with t2:
                    st.code(f"🧬 [a] ALIVE Verified Human\nID: {badge_id}\nVerify: {portal_url}", language="text")

        except Exception as e:
            st.error(f"Error parsing file: {e}")

else:
    # --- ID LOOKUP MODE ---
    st.info("Enter the ALIVE ID found on the post and the text content to verify legitimacy.")
    
    lookup_id = st.text_input("Enter ALIVE ID (e.g., 94-H-a1b2c3-2025):")
    verify_text = st.text_area("Paste the text you are verifying:", height=200)
    
    if st.button("Run Verification"):
        if lookup_id and verify_text:
            # 1. Extract the hash from the ID
            try:
                parts = lookup_id.split("-")
                expected_short_hash = parts[2]
                
                # 2. Hash the pasted text
                actual_hash = hashlib.sha256(verify_text.strip().encode('utf-8')).hexdigest()
                actual_short_hash = actual_hash[:6]
                
                if actual_short_hash == expected_short_hash:
                    st.success(f"✅ LEGITIMATE: This text matches the Fingerprint in ID {lookup_id}")
                    st.markdown(f'<div class="status-header"><div class="pulse"></div> CONTENT AUTHENTIC</div>', unsafe_allow_html=True)
                else:
                    st.error(f"❌ TAMPERED: The text provided does not match ID {lookup_id}")
                    st.write(f"This ID was generated for a different version of this text.")
            except:
                st.error("Invalid ID format. Please use the format: 00-H-XXXXXX-2025")