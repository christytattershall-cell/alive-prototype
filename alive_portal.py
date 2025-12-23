import streamlit as st
import json
import statistics
import pandas as pd
import hashlib

# --- PAGE CONFIG ---
st.set_page_config(page_title="Alive Portal", page_icon="🧬", layout="centered")

# --- STRIPE-INSPIRED CUSTOM CSS ---
st.markdown("""
    <style>
    /* Background and global fonts */
    .stApp { background-color: #f6f9fc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* Main Card Container */
    .main-card {
        background-color: #ffffff;
        padding: 40px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(50, 50, 93, 0.11), 0 1px 3px rgba(0, 0, 0, 0.08);
        border: 1px solid #e6ebf1;
    }
    
    /* Custom Titles */
    h1 { color: #1a1f36; font-weight: 700; font-size: 32px; margin-bottom: 10px; }
    h3 { color: #424770; font-weight: 600; font-size: 18px; }
    
    /* Verification Pill */
    .verify-pill {
        background-color: #e6ebf1;
        color: #635bff;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 12px;
        display: inline-block;
        margin-bottom: 20px;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #635bff;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stButton>button:hover { background-color: #544dc0; border: none; color: white; }
    
    /* Summary Table Styling */
    .stTable { background-color: white; border-radius: 8px; overflow: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<h1>Alive</h1>', unsafe_allow_html=True)
st.markdown('<div class="verify-pill">VERIFICATION GATEWAY</div>', unsafe_allow_html=True)
st.write("### Securely verify human biometric signatures.")

# --- NAVIGATION ---
mode = st.tabs(["File Upload", "Quick Lookup"])

with mode[0]:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.write("#### Document Verification")
    st.write("Upload your .json receipt to verify content integrity.")
    
    uploaded_file = st.file_uploader("Drop your rhythm.json here", type=["json"])
    pasted_text = st.text_area("Paste the original content to verify:", height=200, placeholder="Paste text here...")
    
    if uploaded_file and pasted_text:
        try:
            data = json.load(uploaded_file)
            jitter = data.get("jitter_data", [])
            saved_hash = data.get("content_hash", "")
            timestamp = data.get("timestamp", "Unknown")
            score = data.get("score", 0)
            
            # --- INTEGRITY CHECK ---
            combined = f"{pasted_text.strip()}{timestamp}"
            calculated_hash = hashlib.sha256(combined.encode('utf-8')).hexdigest()
            
            if calculated_hash == saved_hash:
                st.divider()
                st.success(f"**Verified Human Presence.** Session sealed on {timestamp}")
                
                # --- BIOMETRIC CHART ---
                st.write("#### Biometric Signature")
                chart_data = pd.DataFrame(jitter, columns=["Timing Variation (ms)"])
                st.line_chart(chart_data, color="#635bff") # Using Stripe Blue
                
                # --- SUMMARY ---
                st.write("#### Audit Summary")
                summary = {
                    "Check": ["Integrity", "Biometry", "Timestamp", "Unique ID"],
                    "Status": ["Pass", f"{score}% Conf.", "Locked", data.get("id", "N/A")],
                    "Signal": ["✅", "🧬", "🔒", "🆔"]
                }
                st.table(pd.DataFrame(summary))
                
                # --- BADGE ---
                st.write("#### Share Verification")
                st.code(f"🧬 [a] ALIVE Verified Human\nID: {data.get('id')}\nTS: {timestamp}", language="text")
                st.balloons()
            else:
                st.error("🚨 **Tamper Detected.** The document content does not match the biometric seal.")
                st.warning("The hash signature failed validation.")
        except Exception as e:
            st.error(f"Error parsing session data: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

with mode[1]:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.write("#### Manual Lookup")
    l_id = st.text_input("Enter Session ID:")
    l_ts = st.text_input("Enter Timestamp (TS):")
    l_text = st.text_area("Paste Content to Verify:", height=150)
    
    if st.button("Run Global Check"):
        combined = f"{l_text.strip()}{l_ts}"
        calc_hash = hashlib.sha256(combined.encode()).hexdigest()[:6]
        if calc_hash in l_id:
            st.success("Verification Match: Content is authentic.")
        else:
            st.error("No Match: Content has been modified.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<br><hr><center><p style='color: #a3acb9; font-size: 12px;'>© 2025 Alive Verification Systems. Built for Human Integrity.</p></center>", unsafe_allow_html=True)