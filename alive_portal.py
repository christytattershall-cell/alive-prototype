import streamlit as st
import json
import statistics
import pandas as pd
import hashlib
from supabase import create_client, Client # New Database connection

# --- DATABASE CONFIG ---
SUPABASE_URL = "https://ohsyfhzggitmxpubxask.supabase.co"
SUPABASE_KEY = "sb_publishable_iRiMa2IpsJasGGEVWCtpDA_yW1SV7N6"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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
        display: inline-block; width: 15px; height: 15px; background: #00ff00;
        border-radius: 50%; box-shadow: 0 0 10px rgba(0, 255, 0, 1);
        animation: pulse-green 2s infinite; margin-right: 15px; vertical-align: middle;
    }
    @keyframes pulse-green {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 0, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(0, 255, 0, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 0, 0); }
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🧬 ALIVE PORTAL")

# --- 2. MODE SELECTION ---
mode = st.radio("Select Verification Mode:", ["ID Lookup (Cloud Verify)", "File Upload (Legacy)"], horizontal=True)

if mode == "ID Lookup (Cloud Verify)":
    st.info("The new standard: Just enter the ID and the text. We handle the rest.")
    
    lookup_id = st.text_input("Enter ALIVE ID (e.g., 94-H-a1b2c3-2025):")
    verify_text = st.text_area("Paste the text you are verifying:", height=250)
    
    if st.button("VERIFY FROM CLOUD"):
        if lookup_id and verify_text:
            # 1. FETCH FROM SUPABASE
            response = supabase.table("verifications").select("*").eq("id", lookup_id).execute()
            
            if response.data:
                record = response.data[0]
                stored_hash = record['content_hash']
                timestamp = record['timestamp']
                score = record['score']
                
                # 2. VERIFY INTEGRITY (Text + Stored Timestamp)
                combined = f"{verify_text.strip()}{timestamp}"
                calculated_hash = hashlib.sha256(combined.encode('utf-8')).hexdigest()
                
                st.divider()
                
                if calculated_hash == stored_hash:
                    st.markdown(f'<div class="status-header"><div class="pulse"></div> STATUS: VERIFIED HUMAN</div>', unsafe_allow_html=True)
                    st.success(f"✅ AUTHENTIC: This content was signed by a human on {timestamp}")
                    
                    # Show the record details
                    st.metric("Humanity Score", f"{score}%")
                else:
                    st.error("🚨 TAMPER ALERT: The text does not match the original human session.")
                    st.warning("Someone may have edited this content after it was verified.")
            else:
                st.error("❌ ID NOT FOUND: This ID does not exist in the ALIVE registry.")

else:
    st.write("### 📁 Legacy File Upload")
    st.write("Use this if you have the rhythm.json file and want to verify offline.")
    # ... (Your previous file upload code would go here)