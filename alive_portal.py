import streamlit as st
import json
import statistics
import pandas as pd

# (Keep your existing CSS / Pulse styles here...)

# --- NEW SECTION: THE SCIENCE OF THE JITTER ---
if uploaded_file is not None:
    data = json.load(uploaded_file)
    
    if len(data) > 10:
        # Calculate variation (Our 'Humanity' metric)
        variation = statistics.stdev(data)
        score = min(100, int(variation * 500)) 
        
        # --- 1. THE VERDICT ---
        if score > 70:
            st.markdown(f'<div class="status-header"><div class="pulse"></div> STATUS: VERIFIED HUMAN</div>', unsafe_allow_html=True)
            st.metric(label="Humanity Confidence", value=f"{score}%")
            st.success("Biological signature confirmed. Trust established.")
            
            # --- 2. THE VISUAL PROOF (The Graph) ---
            st.write("### Your Biological Jitter")
            # This turns your numbers into a 'mountain range' chart
            chart_data = pd.DataFrame(data[:100], columns=["Rhythm (Seconds)"])
            st.line_chart(chart_data)
            
            st.divider()

            # --- 3. THE BADGE GENERATOR ---
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
            st.error("LOW CONFIDENCE: No biological jitter detected.")
            
    else:
        st.info("The receipt is too small. Write a few more sentences to generate more rhythm data!")