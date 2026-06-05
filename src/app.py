import streamlit as pd
import streamlit as st
import pandas as pd
from log_parser import parse_log_file, detect_threats

# Set page layout to wide mode
st.set_page_config(page_title="Cybersecurity Log Analyzer", layout="wide")

st.title("🔒 Operational Log Analysis & Threat Detection Dashboard")
st.markdown("Upload or analyze server log files to uncover operational anomalies and security threats in real-time.")

LOG_FILE = "data/sample_access.log"

# Load the data using your parser engine
try:
    df = parse_log_file(LOG_FILE)
    brute_suspects, web_attacks = detect_threats(df)
    
    # -----------------------------------------------------------------
    # ROW 1: Key Metrics
    # -----------------------------------------------------------------
    st.subheader("📊 High-Level Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Log Entries", len(df))
    with col2:
        st.metric("Unique IP Addresses", df['ip'].nunique())
    with col3:
        st.metric("Brute Force Alerts", len(brute_suspects))
    with col4:
        st.metric("Web Attack Indicators", len(web_attacks))
        
    st.markdown("---")
    
    # -----------------------------------------------------------------
    # ROW 2: Threat Intelligence Center
    # -----------------------------------------------------------------
    st.subheader("🚨 Threat Intelligence Center")
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.error("Potential Brute Force Targets (/login)")
        if not brute_suspects.empty:
            brute_df = brute_suspects.reset_index()
            brute_df.columns = ["Attacker IP", "Failed Attempts"]
            st.dataframe(brute_df, use_container_width=True)
        else:
            st.success("No brute force attempts detected.")
            
    with col_right:
        st.error("Flagged Web Attack Payloads (SQLi / Directory Traversal)")
        if not web_attacks.empty:
            st.dataframe(web_attacks[['ip', 'method', 'url', 'status']], use_container_width=True)
        else:
            st.success("No web exploit indicators detected.")
            
    st.markdown("---")
    
    # -----------------------------------------------------------------
    # ROW 3: Operational Insights & Traffic Trends
    # -----------------------------------------------------------------
    st.subheader("📈 Traffic Analytics")
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("**Top 10 Most Active IP Addresses**")
        top_ips = df['ip'].value_counts().head(10)
        st.bar_chart(top_ips)
        
    with col_chart2:
        st.markdown("**HTTP Status Code Distribution**")
        status_counts = df['status'].value_counts()
        st.bar_chart(status_counts)

except Exception as e:
    st.error(f"Error loading log file: {e}")