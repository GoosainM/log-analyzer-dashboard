# Operational Log Analysis & Threat Detection Dashboard

An interactive, data-driven security tool built with Python, Pandas, and Streamlit. This application simulates live network infrastructure traffic, parses unformatted server logs using Regular Expressions, and applies analytics logic to flag cyber threats such as Brute-Force actions and Web Exploits (SQL Injection/Directory Traversal).

## 🚀 Features
- **Synthetic Log Generation:** Simulates an Apache/Nginx environment injecting both organic traffic and malicious footprints.
- **Regex Parsing Engine:** Tokenizes unstructured text logs directly into clean Pandas DataFrames.
- **Threat Intelligence Center:** Automatically flags high-frequency authentication failures (`401 Unauthorized`) and malicious URL payloads.
- **Interactive Visualizations:** High-level metric cards and real-time behavioral charts built with Streamlit.

## 🛠️ Tech Stack
- **Language:** Python
- **Data Analytics:** Pandas
- **UI Framework:** Streamlit
- **Data Simulation:** Faker, Regex (`re`)

## 📦 Setup & Installation
1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt