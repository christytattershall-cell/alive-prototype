import streamlit as st
import json
import statistics
import pandas as pd
import hashlib

st.set_page_config(page_title="ALIVE Portal", page_icon="🧬")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .status-header { font-family: monospace; color: #00ff00; font-size: 26px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧬 ALIVE PORTAL")

mode = st.radio("Verification Method:", ["File Upload (JSON)", "Manual ID Lookup"], horizontal=True)

if mode == "File Upload (JSON)":
    uploaded_file = st.file_uploader("Upload rhythm.json", type=["json"])
    pasted_text = st.text_area("Paste text to verify:")

    if uploaded_file and pasted_text:
        data = json.load(uploaded_file)
        ts = data.get("timestamp")
        
        # Verify Lock
        combined = f"{pasted_text.strip()}{ts}"
        current_hash = hashlib.sha256(combined.encode()).hexdigest()
        
        if current_hash == data.get("content_hash"):
            st.success(f"VERIFIED HUMAN. Created on: {ts}")
            st.metric("Humanity Score", f"{data.get('score')}%")
        else:
            st.error("TAMPER ALERT: Content or time mismatch.")

else:
    st.info("Paste the ID, Timestamp, and Text from the post to verify.")
    l_id = st.text_input("Enter ALIVE ID:")
    l_ts = st.text_input("Enter Timestamp (TS):")
    l_text = st.text_area("Paste the Content:")

    if st.button("VERIFY"):
        combined = f"{l_text.strip()}{l_ts}"
        calc_hash = hashlib.sha256(combined.encode()).hexdigest()[:6]
        
        if calc_hash in l_id:
            st.success("AUTHENTIC CONTENT: Matches the human signature.")
        else:
            st.error("MISMATCH: This content has been altered.")