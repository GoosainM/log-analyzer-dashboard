# 🚀 Cross-Disciplinary Engineering Suite: Performance Analytics & Security Operations

Welcome to my production deployment repository. This workspace showcases the intersection of robust backend automation, cybersecurity tooling, and advanced athletic data pipelines. Each application is fully containerized and deployed live in the cloud.

---

## 🛠️ Global Architecture & Tech Stack
* **Language:** Python 3.10+
* **Frontend UI Framework:** Streamlit (Cloud Deployed)
* **Data Processing:** Pandas, NumPy, Vectorized Arrays
* **Document Automation Engine:** ReportLab (Programmatic Dynamic PDF Generation)
* **Security & Network Layer:** Advanced Regular Expressions (RegEx), WHOIS Protocol Client Execution
* **Version Control & CI/CD:** Git, GitHub Webhooks, Automated Cloud Instantiation

---

## 🔬 Featured Live Applications

### 1. 🏋️‍♂️ HYROX Work Capacity & Performance Engine
* **Live Web App:** [https://hyrox-lab.streamlit.app](https://hyrox-lab.streamlit.app)
* **Core Module:** `src/hyrox_app.py`
* **Architecture:** Engineered a specialized concurrent-training analytics suite designed for competitive hybrid athletes.
* **Key Mechanisms:**
  * **Compromised Pacing Analytics:** Tracks degradation trends in 1km running splits when interspersed with high-intensity structural stations (Sled Pushes, Burpee Broad Jumps, Wall Balls).
  * **Autonomic Nervous System Diagnostic:** Runs real-time evaluation logic against athlete biometric markers—specifically Heart Rate Variability (HRV) and resting heart rates—to catch central nervous system (CNS) overreaching.
  * **Programmatic Blueprint Generation:** Integrates an automated document compilation pipeline that outputs a crisp, corporate-styled PDF athletic scorecard on user command.

### 2. 🏃‍♂️ Endurance Performance & Adaptive Analytics Lab
* **Live Web App:** [https://performance-lab.streamlit.app](https://performance-lab.streamlit.app)
* **Core Module:** `src/fitness_app.py`
* **Architecture:** Built an intake, data visualization, and predictive target-modeling platform focused on volume and velocity optimization for long-distance runners.
* **Key Mechanisms:**
  * **Algorithmic Progressive Overload:** Implements mathematical constraint matrices restricting automated weekly training volume increases strictly within a medically safe 10% ceiling to eliminate stress injury markers.
  * **Predictive Milestone Runway:** Dynamically maps current multi-week base metrics against long-term targets (e.g., Marathon builds or Pace optimization schedules) using real-time interactive Pandas charts.

### 3. 💻 Cyber Threat & Log Analyzer Hub
* **Live Web App:** [https://log-analyzer-dashboard.streamlit.app](https://log-analyzer-dashboard.streamlit.app)
* **Core Modules:** `src/log_parser.py`, `src/osint_app.py`
* **Architecture:** Formulated a Security Operations Center (SOC) utility designed to process raw, unstructured production server log streams and translate them into visible threat vectors.
* **Key Mechanisms:**
  * **Regex Threat Parsing:** Utilizes high-performance string matching to scan, group, and isolate malicious IP signatures, broken network hooks, and request vectors.
  * **OSINT Passive Investigation Layer:** Leverages low-level socket-based protocol clients to coordinate external domain queries (WHOIS records) natively within a secure console environment.

---

## ⚡ Local Setup & Installation

To run any of the performance analytics modules or security dashboards locally on your machine, clone the repository and run the setup sequence below:

```bash
# Clone the workspace
git clone [https://github.com/GoosainM/log-analyzer-dashboard.git](https://github.com/GoosainM/log-analyzer-dashboard.git)
cd log-analyzer-dashboard

# Install localized production dependencies
pip install -r requirements.txt

# Run the Hyrox Performance Lab locally
python -m streamlit run src/hyrox_app.py

# Run the Running Analytics Lab locally
python -m streamlit run src/fitness_app.py