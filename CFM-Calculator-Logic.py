import streamlit as st
import pandas as pd

st.set_page_config(page_title="CFM & Case Airflow Calculator", layout="wide")
st.title("💨 Case & Server Cooling CFM & Static Pressure Calculator")

st.markdown("""
Use this tool to calculate airflow dynamics for PC builds, workstations, or server rooms. Enter fan specifications below or use preconfigured templates.

- **CFM**: Cubic Feet per Minute (airflow)
- **Static Pressure**: Ability to push through obstructions (e.g., mesh, filters, rack walls)
- **Wattage & Noise**: Power and acoustic levels

### Pressure Strategy:
- 🔴 **Negative Pressure**: More exhaust. Best thermal reduction. Requires dust filtering.
- 🟢 **Positive Pressure**: More intake. Keeps out dust. Watch for heat pockets.
- ⚪ **Neutral Pressure**: Balanced flow. Low turbulence, but not always efficient.

### Airflow Design Applies to Both PCs and Server Rooms:
- Think of a **server room as a PC case**:
  - Servers = hardware components (CPU/GPU)
  - Raised floors & racks = cable pathways & airflow corridors
  - Fans in walls, ceilings, and AC ducts = intake & exhaust
  - **Cold air at floor level, hot air rises to ceiling exhaust**
""")

# --- Template Loader ---
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

default = load_template(template)

# --- Input Tables ---
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
