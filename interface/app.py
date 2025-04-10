import os
import streamlit as st

# Use an environment variable for the stable public URL (e.g., provided by your reverse proxy)
# For local testing, use "http://localhost:8080"
REVERSE_PROXY_URL = os.environ.get("REVERSE_PROXY_URL", "http://localhost:8080")

st.title("Central Interface Dashboard")

# Sidebar navigation for app selection
st.sidebar.header("Navigate to an App")
app_choice = st.sidebar.selectbox("Choose an app", ["Home", "logP Calculator", "LLE Calculator"])

if app_choice == "Home":
    st.write("Welcome to the central dashboard. Use the sidebar to select an app to access.")

elif app_choice == "logP Calculator":
    st.header("logP Calculator")
    st.write("Click the link below to open the logP Calculator.")
    # Build the URL using the reverse proxy's public endpoint and the predefined path
    app_logP_url = f"{REVERSE_PROXY_URL}/app_logP_Calculator/"
    # Render an HTML link that opens in a new tab
    st.markdown(f'<a href="{app_logP_url}" target="_blank">Open logP Calculator</a>', unsafe_allow_html=True)

elif app_choice == "LLE Calculator":
    st.header("LLE Calculator")
    st.write("Click the link below to open the LLE Calculator.")
    app_LLE_url = f"{REVERSE_PROXY_URL}/app_LLE_Calculator/"
    st.markdown(f'<a href="{app_LLE_url}" target="_blank">Open LLE Calculator</a>', unsafe_allow_html=True)
