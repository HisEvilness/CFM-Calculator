import streamlit as st
import pandas as pd
import json
import plotly.express as px

st.set_page_config(page_title="CFM & Case Airflow Calculator", layout="wide")
st.title("💨 Case & Server Cooling CFM & Static Pressure Calculator")

st.markdown("""
Use this tool to calculate airflow dynamics for PC builds, workstations, or server rooms. Enter fan specifications below or use preconfigured templates.

- **CFM**: Cubic Feet per Minute (airflow)
- **Static Pressure**: Ability to push through obstructions (e.g., mesh, filters, rack walls)
- **Wattage & Noise**: Power and acoustic levels

### Volume Conversion:
Enter your case or room volume to estimate air replacement needs.
""")

st.markdown("---")
st.subheader("📏 Room/Case Volume")

col_v1, col_v2 = st.columns(2)

with col_v1:
    volume_liters = st.number_input("Enter volume in Liters (L)", min_value=0.0, value=100.0, step=10.0, format="%.2f")
    volume_m3 = volume_liters / 1000

with col_v2:
    volume_m3_input = st.number_input("Or enter volume in Cubic Meters (m³)", min_value=0.0, value=volume_m3, step=0.1, format="%.3f")
    if volume_m3_input != volume_m3:
        volume_liters = volume_m3_input * 1000
        volume_m3 = volume_m3_input

st.write(f"📦 Volume: **{volume_liters:.2f} L** / **{volume_m3:.3f} m³**")

st.markdown("""
---
### ⚡ Air Replacement Efficiency
This estimates how fast your airflow can cycle the total air in your space:
- 1 m³ = 35.3147 ft³
- CFM = Cubic Feet per Minute
""")

@st.cache_data
def load_templates():
    return json.load(open("templates.json"))

templates = load_templates()

st.sidebar.header("💡 Load Template")
template_name = st.sidebar.selectbox("Choose a system layout:", ["None"] + list(templates.keys()))
fan_cols = ["Fan Name", "Static Pressure (mmH2O)", "CFM", "Watts Low", "Watts High", "dB Low", "dB High"]

default_df = pd.DataFrame(columns=fan_cols)
if template_name != "None":
    default_df = pd.DataFrame(templates[template_name], columns=fan_cols)

# Fan input
tabs = st.tabs(["Intake Fans", "Exhaust Fans", "Hardware/Server Nodes"])

with tabs[0]:
    st.subheader("Intake Fans")
    intake_df = st.data_editor(default_df.head(3), num_rows="dynamic", key="intake")

with tabs[1]:
    st.subheader("Exhaust Fans")
    exhaust_df = st.data_editor(default_df.iloc[3:5], num_rows="dynamic", key="exhaust")

with tabs[2]:
    st.subheader("Hardware/Server Cooling Units")
    hardware_df = st.data_editor(default_df.iloc[5:], num_rows="dynamic", key="hardware")

# Calculation logic
def calc_totals(df):
    return {
        "Total CFM": df["CFM"].sum(),
        "Total Watts Low": df["Watts Low"].sum(),
        "Total Watts High": df["Watts High"].sum(),
        "Avg dB": df[["dB Low", "dB High"]].mean(axis=1).mean()
    }

intake_stats = calc_totals(intake_df)
exhaust_stats = calc_totals(exhaust_df)
hardware_stats = calc_totals(hardware_df)

# Airflow and pressure logic
total_airflow_cfm = intake_stats['Total CFM'] + exhaust_stats['Total CFM']
cfm_diff = intake_stats['Total CFM'] - exhaust_stats['Total CFM']
pressure_type = "Neutral"
color = "#1f77b4"  # Blue
if cfm_diff > 10:
    pressure_type = "Positive"
    color = "#2ca02c"  # Green
elif cfm_diff < -10:
    pressure_type = "Negative"
    color = "#d62728"  # Red

optimal_cfm = hardware_stats['Total CFM'] * 1.25
surplus_airflow = total_airflow_cfm - hardware_stats['Total CFM']

# Volume & ACH
volume_ft3 = volume_m3 * 35.3147
if volume_ft3 > 0:
    air_cycles_per_minute = total_airflow_cfm / volume_ft3
    air_cycles_per_hour = air_cycles_per_minute * 60
    st.metric("Air Cycles Per Minute", f"{air_cycles_per_minute:.2f}")
    st.metric("Air Cycles Per Hour (ACH)", f"{air_cycles_per_hour:.1f}")
else:
    st.warning("Please enter a valid volume to calculate air replacement.")

# Metrics Output
st.markdown("---")
st.header("📊 Cooling Performance Summary")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Intake CFM", f"{intake_stats['Total CFM']:.2f}")
    st.metric("Avg Intake Noise", f"{intake_stats['Avg dB']:.1f} dB")
with col2:
    st.metric("Exhaust CFM", f"{exhaust_stats['Total CFM']:.2f}")
    st.metric("Avg Exhaust Noise", f"{exhaust_stats['Avg dB']:.1f} dB")
with col3:
    st.metric("Hardware Cooling CFM", f"{hardware_stats['Total CFM']:.2f}")

st.subheader("🔍 Analysis")
st.markdown(f"<div style='background-color:{color}; padding: 10px; border-radius: 5px; color: white;'>"
            f"<b>Detected Pressure Type:</b> {pressure_type} Pressure ({cfm_diff:+.2f} CFM)"
            f"</div>", unsafe_allow_html=True)

st.write(f"**Surplus vs Hardware CFM**: {surplus_airflow:.2f} CFM")
st.write(f"**Optimal Target (125% of Hardware/Server CFM)**: {optimal_cfm:.2f} CFM")

# Flow Chart using Plotly
st.subheader("🔄 Airflow Distribution Chart")
cfm_chart = pd.DataFrame({
    "Type": ["Intake", "Exhaust", "Hardware"],
    "CFM": [intake_stats['Total CFM'], exhaust_stats['Total CFM'], hardware_stats['Total CFM']]
})
fig = px.bar(cfm_chart, x="Type", y="CFM", color="Type", text="CFM",
             color_discrete_sequence=["#1f77b4", "#d62728", "#ff7f0e"], title="CFM Comparison")
st.plotly_chart(fig, use_container_width=True)

st.caption("These figures estimate how often the air in the case or room is fully replaced.")

st.markdown("""
---
**Author**: Paul "HisEvilness" Ripmeester  
[Case Airflow Guide Part I](https://www.hisevilness.com/articles/tech-oc-ing-seo-and-more/case-airflow-best-cooling-practises.html)  
[Case Airflow Guide Part II](https://www.hisevilness.com/articles/technology/case-airflow-best-cooling-practices-part-ii.html?showall=1)
""")
