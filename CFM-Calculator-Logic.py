import streamlit as st
import pandas as pd

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

# Template Loader
st.sidebar.header("💡 Load Template")
template = st.sidebar.selectbox(
    "Choose a system layout:",
    ["None", "Mid-Tower Gaming PC", "Overclocked Workstation", "Server Rack (3U Nodes)", "Server Room (6 Rack Rows)"]
)

fan_cols = ["Fan Name", "Static Pressure (mmH2O)", "CFM", "Watts Low", "Watts High", "dB Low", "dB High"]

def load_template(name):
    if name == "Mid-Tower Gaming PC":
        return pd.DataFrame([
            ["Front Fan 1", 1.5, 45, 5, 8, 20, 26],
            ["Top Fan 1", 1.2, 50, 6, 9, 22, 28],
            ["Rear Fan", 1.3, 48, 5, 7, 21, 27],
            ["GPU Cooling", 2.1, 30, 10, 18, 28, 36],
            ["CPU Cooler", 2.8, 35, 8, 12, 25, 32],
        ], columns=fan_cols)
    elif name == "Overclocked Workstation":
        return pd.DataFrame([
            ["Front Fan 1", 2.0, 65, 7, 11, 22, 30],
            ["Front Fan 2", 2.0, 65, 7, 11, 22, 30],
            ["Top Fan", 1.4, 60, 6, 10, 23, 31],
            ["Rear Fan", 1.6, 55, 5, 9, 24, 30],
            ["CPU AIO", 3.0, 40, 15, 25, 30, 40],
            ["GPU Fans", 2.5, 50, 10, 15, 26, 35]
        ], columns=fan_cols)
    elif name == "Server Rack (3U Nodes)":
        return pd.DataFrame([
            ["Rack Front Intake", 3.2, 90, 12, 18, 35, 45],
            ["Rack Rear Exhaust", 2.8, 95, 13, 20, 36, 48],
            ["Node 1 CPU", 4.0, 40, 10, 16, 30, 38],
            ["Node 2 CPU", 4.0, 40, 10, 16, 30, 38],
            ["Node 3 CPU", 4.0, 40, 10, 16, 30, 38]
        ], columns=fan_cols)
    elif name == "Server Room (6 Rack Rows)":
        return pd.DataFrame([
            ["Floor Intake Grid", 2.5, 500, 30, 60, 40, 55],
            ["Ceiling Exhaust Grid", 2.0, 520, 32, 64, 42, 57],
            ["Rack Row 1", 3.8, 150, 20, 30, 34, 45],
            ["Rack Row 2", 3.8, 150, 20, 30, 34, 45],
            ["Rack Row 3", 3.8, 150, 20, 30, 34, 45],
            ["Rack Row 4", 3.8, 150, 20, 30, 34, 45],
            ["Rack Row 5", 3.8, 150, 20, 30, 34, 45],
            ["Rack Row 6", 3.8, 150, 20, 30, 34, 45]
        ], columns=fan_cols)
    else:
        return pd.DataFrame(columns=fan_cols)

def calc_totals(df):
    return {
        "Total CFM": df["CFM"].sum(),
        "Total Watts Low": df["Watts Low"].sum(),
        "Total Watts High": df["Watts High"].sum(),
        "Avg dB": df[["dB Low", "dB High"]].mean(axis=1).mean()
    }

default = load_template(template)
tabs = st.tabs(["Intake Fans", "Exhaust Fans", "Hardware/Server Nodes"])

with tabs[0]:
    st.subheader("Intake Fans")
    intake_df = st.data_editor(default.head(3), num_rows="dynamic", key="intake")

with tabs[1]:
    st.subheader("Exhaust Fans")
    exhaust_df = st.data_editor(default.iloc[3:5], num_rows="dynamic", key="exhaust")

with tabs[2]:
    st.subheader("Hardware/Server Cooling Units")
    hardware_df = st.data_editor(default.iloc[5:], num_rows="dynamic", key="hardware")

intake_stats = calc_totals(intake_df)
st.session_state.intake_stats = intake_stats
exhaust_stats = calc_totals(exhaust_df)
st.session_state.exhaust_stats = exhaust_stats
hardware_stats = calc_totals(hardware_df)

total_airflow_cfm = intake_stats['Total CFM'] + exhaust_stats['Total CFM']
volume_ft3 = volume_m3 * 35.3147

if volume_ft3 > 0:
    air_cycles_per_minute = total_airflow_cfm / volume_ft3
    air_cycles_per_hour = air_cycles_per_minute * 60
    st.metric("Air Cycles Per Minute", f"{air_cycles_per_minute:.2f}")
    st.metric("Air Cycles Per Hour (ACH)", f"{air_cycles_per_hour:.1f}")
else:
    st.warning("Please enter a valid volume to calculate air replacement.")

cfm_diff = intake_stats['Total CFM'] - exhaust_stats['Total CFM']
pressure_type = "Neutral"
if cfm_diff > 10:
    pressure_type = "Positive"
elif cfm_diff < -10:
    pressure_type = "Negative"

optimal_cfm = hardware_stats['Total CFM'] * 1.25
surplus_airflow = total_airflow_cfm - hardware_stats['Total CFM']

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
st.write(f"**Detected Pressure Type**: {pressure_type} Pressure ({cfm_diff:+.2f} CFM)")
st.write(f"**Surplus vs Hardware CFM**: {surplus_airflow:.2f} CFM")
st.write(f"**Optimal Target (125% of Hardware/Server CFM)**: {optimal_cfm:.2f} CFM")

st.caption("These figures estimate how often the air in the case or room is fully replaced.")

st.markdown("""
---
**Author**: Paul "HisEvilness" Ripmeester  
[Case Airflow Guide Part I](https://www.hisevilness.com/articles/tech-oc-ing-seo-and-more/case-airflow-best-cooling-practises.html)  
[Case Airflow Guide Part II](https://www.hisevilness.com/articles/technology/case-airflow-best-cooling-practices-part-ii.html?showall=1)
""")
