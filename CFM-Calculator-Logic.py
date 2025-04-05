import streamlit as st
import pandas as pd

st.set_page_config(page_title="CFM & Case Airflow Calculator", layout="wide")
st.title("💨 Case Cooling CFM & Static Pressure Calculator")

st.markdown("""
Use this tool to calculate airflow dynamics for PC builds. Enter fan specifications below.

- **CFM**: Cubic Feet per Minute (airflow)
- **Static Pressure**: Ability to push through obstructions
- **Wattage & Noise**: Power and sound levels

---
""")

# Section 1: Input Tables
tabs = st.tabs(["Intake Fans", "Exhaust Fans", "Hardware Fans"])

fan_cols = ["Fan Name", "Static Pressure (mmH2O)", "CFM", "Watts Low", "Watts High", "dB Low", "dB High"]

with tabs[0]:
    st.subheader("Intake Fans")
    intake_df = st.data_editor(pd.DataFrame(columns=fan_cols), num_rows="dynamic", key="intake")

with tabs[1]:
    st.subheader("Exhaust Fans")
    exhaust_df = st.data_editor(pd.DataFrame(columns=fan_cols), num_rows="dynamic", key="exhaust")

with tabs[2]:
    st.subheader("Hardware Fans (GPU, CPU, AIO)")
    hardware_df = st.data_editor(pd.DataFrame(columns=fan_cols), num_rows="dynamic", key="hardware")

# Section 2: Calculations

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

# Section 3: Output Results
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

# Airflow Pressure Logic
cfm_diff = intake_stats['Total CFM'] - exhaust_stats['Total CFM']
pressure_type = "Neutral"
if cfm_diff > 10:
    pressure_type = "Positive"
elif cfm_diff < -10:
    pressure_type = "Negative"

optimal_cfm = hardware_stats['Total CFM'] * 1.25
surplus_airflow = intake_stats['Total CFM'] + exhaust_stats['Total CFM'] - hardware_stats['Total CFM']

st.subheader("🔍 Analysis")
st.write(f"**Pressure Type**: {pressure_type} Pressure ({cfm_diff:+.2f} CFM)")
st.write(f"**Surplus vs Hardware CFM**: {surplus_airflow:.2f} CFM")
st.write(f"**Optimal Target (125% of Hardware CFM)**: {optimal_cfm:.2f} CFM")

if surplus_airflow < 0:
    st.warning("⚠️ Airflow is insufficient. Consider adding more fans.")
elif surplus_airflow > optimal_cfm:
    st.info("ℹ️ Airflow may be excessive and could cause turbulence.")
else:
    st.success("✅ Airflow is within optimal range.")

# Footer
st.markdown("""
---
**Author**: Paul "HisEvilness" Ripmeester  
[Case Airflow Guide](https://www.hisevilness.com/articles/technology/case-airflow-best-cooling-practices-part-ii.html?showall=1)
""")
