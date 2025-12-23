import streamlit as st
import json
import statistics
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="ALIVE Portal", page_icon="🧬", layout="centered")

# --- 1. CUSTOM CSS (The Cyber Aesthetic) ---
st.markdown("""
    <style>
    /* Main Background and Text */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Terminal-style headers */
    .status-header {
        font-family: 'Courier New', Courier, monospace;
        color: #00ff00;
        font-size: 26px;
        font-weight: bold;
        letter-spacing: 2px;
        padding: 10px 0;
    }

    /* Pulse animation for the Verified Human status */
    .pulse {
        display: inline-block;
        width: 15px;
        height: 15px;
        background: #00ff00;
        border-radius: 50%;
        box-shadow: 0 0 0 0 rgba(0, 255, 0, 1);
        animation: pulse-green 2s infinite;
        margin-right: 15px;
    }

    @keyframes pulse-green {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 0, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(0, 255, 0, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 0, 0); }
    }

    /* Style the File Uploader Box */
    [data-testid="stFileUploader"] {
        border: 2px solid #000000;
        padding: 20px;
        border-radius: 10px;
        background-color: #A9A9A9;
    }

    /* Change Button Look */
    button[kind="secondary"] {
        background-color: #00ff00 !important;
        color: black !important;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HEADER SECTION ---
st.title("🧬 ALIVE PORTAL")
st.write("---")
st.write("### BIOMETRIC VERIFICATION")
st.info("Upload your rhythm data to analyze biological jitter and confirm humanity.")

# --- 3. THE FIX: DEFINE THE UPLOADER VARIABLE ---
# This ensures 'uploaded_file' exists before we try to use it.
uploaded_file = st.file_uploader("Drop rhythm.json here", type=["json"])

# --- 4. THE SCIENCE OF THE JITTER ---
if uploaded_file is not None:
    # Load the data from the uploaded JSON
    data = json.load(uploaded_file)
    
    if len(data) > 10:
        # Calculate variation (Our 'Humanity' metric)
        # Human movement/typing has subtle, irregular gaps that AI lacks.
        variation = statistics.stdev(data)
        score = min(100, int(variation * 500)) 
        
        # --- THE VERDICT ---
        if score > 70:
            st.markdown(f'<div class="status-header"><div class="pulse"></div> STATUS: VERIFIED HUMAN</div>', unsafe_allow_html=True)
            
            # Display metrics
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Humanity Confidence", value=f"{score}%", delta="UNSIMULATABLE")
            with col2:
                st.metric(label="Biological Jitter", value=f"{variation:.4f}s")
                
            st.success("Biological signature confirmed. Trust established.")
            
            # --- VISUAL PROOF (The Graph) ---
            st.write("### 🧬 Your Biological Jitter")
            st.write("This graph visualizes the millisecond variations in your input rhythm.")
            chart_data = pd.DataFrame(data[:100], columns=["Rhythm (Seconds)"])
            st.line_chart(chart_data, color="#00ff00")
            
            st.divider()

            # --- THE BADGE GENERATOR ---
            st.write("### 🛡️ Get Your H-Mark Badge")
            st.write("Copy the code below and paste it into the 'Custom HTML' block of your blog or website.")
            
            # CHANGE THIS URL to your actual live Streamlit link!
            my_portal_url = "https://alive-prototype.streamlit.app/" 
            
            badge_code = f"""<div style="padding:15px; border:2px solid #00ff00; border-radius:10px; background-color:#1a1c24; text-align:center;">
    <a href="{my_portal_url}" style="color:#00ff00; text-decoration:none; font-family:monospace; font-weight:bold;">
        [a] ALIVE CERTIFIED HUMAN | ID: {score}-H-2025
    </a>
</div>"""

            # This shows the box they can copy
            st.code(badge_code, language="html")
            
            st.write("This badge acts as a direct link back to this portal, proving to your readers that this specific post was authored by a human.")
            st.balloons()
            
        else:
            st.error("LOW CONFIDENCE: No biological jitter detected. Analysis suggests automated input.")
            st.warning("Ensure you are providing raw, unedited rhythm data.")
            
    else:
        st.info("The receipt is too small. Provide a larger data sample to generate more rhythm data!")
else:
    # This shows when no file is uploaded yet
    st.write("Waiting for data stream... 📡")