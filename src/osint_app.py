import streamlit as st
import requests
import whois
import base64
from datetime import datetime

# Configure Page
st.set_page_config(page_title="Bulk OSINT Investigator", layout="wide")
st.title("🔍 Bulk OSINT Link & Domain Investigator")
st.markdown("Analyze URLs and domains simultaneously for registration history and live security threat intelligence.")

# Secure your API key input
VT_API_KEY = st.sidebar.text_input("Enter VirusTotal API Key", type="password", help="Get a free key from virustotal.com")

def analyze_domain_age(domain):
    """Fetches WHOIS data to determine the age and risk profile of a domain."""
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date
        
        # Handle cases where creation_date is a list of multiple dates
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
            
        if creation_date:
            age_days = (datetime.now() - creation_date).days
            return {
                "Created": creation_date.strftime("%Y-%m-%d"),
                "Registrar": w.registrar or "Unknown",
                "Age (Days)": age_days,
                "Risk Alert": "🚨 High Risk (New Domain)" if age_days < 90 else "✅ Low Risk (Established)"
            }
    except Exception:
        return {"Created": "Unknown", "Registrar": "Unknown", "Age (Days)": "Unknown", "Risk Alert": "⚠️ No WHOIS Data Found"}
    return {"Created": "Unknown", "Registrar": "Unknown", "Age (Days)": "Unknown", "Risk Alert": "⚠️ No WHOIS Data Found"}

def check_virustotal_url(url, api_key):
    """Queries VirusTotal API for scanning and reputation metrics using a URL."""
    if not api_key:
        return {"Status": "Missing API Key", "Malicious Hits": 0, "Total Scanners": 0}
        
    try:
        # VirusTotal requires URLs to be encoded in base64 without padding
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        endpoint = f"https://www.virustotal.com/api/v3/urls/{url_id}"
        headers = {"x-apikey": api_key}
        
        response = requests.get(endpoint, headers=headers)
        
        if response.status_code == 200:
            stats = response.json()['data']['attributes']['last_analysis_stats']
            return {
                "Status": "Clean" if stats['malicious'] == 0 else "🚨 Malicious",
                "Malicious Hits": stats['malicious'],
                "Total Scanners": sum(stats.values())
            }
        elif response.status_code == 404:
            return {"Status": "Not Scanned Yet", "Malicious Hits": 0, "Total Scanners": 0}
    except Exception:
        return {"Status": "API Error", "Malicious Hits": 0, "Total Scanners": 0}
    return {"Status": "Error", "Malicious Hits": 0, "Total Scanners": 0}

# --- UI Layout ---
st.subheader("1. Input Target Links/Domains")
user_input = st.text_area("Paste links or domains to investigate (one per line):", 
                          placeholder="example.com\nhttps://google.comnsuspicious-link.net")

if st.button("Run Global OSINT Triage"):
    if not user_input.strip():
        st.warning("Please paste at least one domain or link to analyze.")
    else:
        # Split inputs cleanly into a list
        targets = [line.strip() for line in user_input.split("\n") if line.strip()]
        
        st.subheader("📊 Investigation Results")
        
        # Loop over every target provided dynamically
        for target in targets:
            # Clean up the target string to get the bare domain for WHOIS lookup
            clean_domain = target.replace("https://", "").replace("http://", "").split("/")[0]
            
            with st.expander(f"🔎 Reporting File: {target}", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🌐 Domain Registration Insight (WHOIS)**")
                    whois_data = analyze_domain_age(clean_domain)
                    st.write(f"**Age:** {whois_data['Age (Days)']} Days")
                    st.write(f"**Registered on:** {whois_data['Created']}")
                    st.write(f"**Registrar:** {whois_data['Registrar']}")
                    st.write(f"**Status:** {whois_data['Risk Alert']}")
                    
                with col2:
                    st.markdown("**🛡️ Global Threat Intelligence (VirusTotal)**")
                    if VT_API_KEY:
                        vt_data = check_virustotal_url(target, VT_API_KEY)
                        st.write(f"**Verdict:** {vt_data['Status']}")
                        st.write(f"**Flagged By:** {vt_data['Malicious Hits']} / {vt_data['Total Scanners']} security providers")
                    else:
                        st.info("💡 Add a VirusTotal API Key in the left sidebar to activate multi-engine intelligence scanning.")