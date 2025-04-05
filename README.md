💨 CFM & Case Airflow Calculator (Alpha)
A technical airflow modeling tool built in Streamlit for use in PC builds, workstations, server racks, and datacenter cooling layouts. This calculator provides a performance overview based on fan data, volume metrics, and airflow pressure balancing — designed for overclockers, IT planners, and thermal engineers.

🔗 Live Demo: https://cfm-calculator.streamlit.app

✅ Alpha Features
📏 Volume Input

Supports both Liters (L) and Cubic Meters (m³)

Auto-conversion between units

💨 Airflow Calculations

Dynamic editing of intake, exhaust, and hardware fans

Tracks CFM, static pressure, power draw, and dB ranges

Calculates overall system airflow and pressure direction

🧠 Pressure Type Detection

Automatically classifies configuration as:
🔴 Negative pressure
🟢 Positive pressure
🔵 Neutral pressure

🔁 ACH (Air Change per Hour)

Uses fan CFM vs. case volume (m³) to compute:

Air Cycles per Minute (ACM)

Air Changes per Hour (ACH)

📊 Visual Output

Native bar chart to compare intake, exhaust, and hardware cooling

Color-coded pressure detection block (based on airflow balance)

📁 Template Loading

Loads predefined templates from external templates.json

Current presets include:

Mini PC

Office PC

Gaming PC

High-End Gaming PC

Workstation

Home Server Rack

Datacenter Rack – Medium

Datacenter Rack – Full Row

📦 Technology Stack
streamlit (no extra frontend libraries)

pandas for table logic

json for template import

No Plotly, Matplotlib, or unsupported packages (Streamlit Cloud ready)

📂 File Structure
cfm-calculator/
├── CFM-Calculator-Logic.py # Streamlit app logic
├── templates.json # Airflow configuration templates
├── requirements.txt # Dependencies for deployment
└── README.md # This file

🛠 Getting Started
Clone the repository or download the project

Ensure your environment includes:

streamlit>=1.25.0
pandas>=1.5.0

Run locally:

streamlit run CFM-Calculator-Logic.py

Make sure the file templates.json is in the same folder as the script.

📌 Known Limitations (Alpha Stage)
No export functionality yet (CSV/JSON)

No template editor (currently JSON-only)

No multi-zone airflow layout simulation

No real-time fan curve or thermal feedback

These are planned for the Beta milestone.

👨‍💻 Author & Reference
Paul "HisEvilness" Ripmeester
Founder – Infinity Fabric LLC
www.hisevilness.com

Reference Articles:

Best Cooling Practices – Part I:
https://www.hisevilness.com/articles/tech-oc-ing-seo-and-more/case-airflow-best-cooling-practises.html

Best Cooling Practices – Part II:
https://www.hisevilness.com/articles/technology/case-airflow-best-cooling-practices-part-ii.html?showall=1

🧭 License
Released under Infinity Fabric LLC
Commercial use requires attribution and written consent.
