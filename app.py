import streamlit as st
import pandas as pd
from datetime import datetime
from utils import calculate_emissions, generate_unique_id
from generate_certificate import generate_certificate_pdf

# Config
st.set_page_config(page_title="Zeromoto Credit Tracker", layout="wide")
st.title("🪙 Zeromoto Carbon Credit Tracker")
st.caption("Track your climate impact. Earn credits. Download proof.")

# Session init
if "trip_data" not in st.session_state:
    st.session_state.trip_data = []
if "partner_name" not in st.session_state:
    st.session_state.partner_name = ""

# Input: Partner name
st.sidebar.header("Partner Information")
partner_name = st.sidebar.text_input("Partner Name / Company", value=st.session_state.partner_name)
st.session_state.partner_name = partner_name

# Upload CSV
st.header("📥 Upload Trip Log")
csv = st.file_uploader("Upload CSV (Date, Scooter ID, Distance (km), Vehicle Type)", type="csv")
if csv:
    df = pd.read_csv(csv)
    enriched = []

    for _, row in df.iterrows():
        emitted, avoided, factor = calculate_emissions(row["Distance (km)"], row["Vehicle Type"])
        enriched.append({
            "Date": row["Date"],
            "Scooter ID": row["Scooter ID"],
            "Distance (km)": row["Distance (km)"],
            "Vehicle Type": row["Vehicle Type"],
            "Emission Factor": factor,
            "CO₂ Emitted (kg)": emitted,
            "CO₂ Avoided (kg)": avoided
        })

    st.session_state.trip_data = enriched
    st.success(f"{len(enriched)} trips processed.")

# Manual trip entry
st.header("📝 Manually Add a Trip")
with st.form("manual_trip_form"):
    manual_date = st.date_input("Trip Date", value=datetime.today())
    manual_scooter = st.text_input("Scooter ID")
    manual_distance = st.number_input("Distance (km)", min_value=0.0, step=0.1)
    manual_vehicle = st.selectbox("Vehicle Type", list(EMISSION_FACTORS.keys()))
    submit_manual = st.form_submit_button("Add Trip")

    if submit_manual:
        emitted, avoided, factor = calculate_emissions(manual_distance, manual_vehicle)
        st.session_state.trip_data.append({
            "Date": manual_date.strftime("%Y-%m-%d"),
            "Scooter ID": manual_scooter or "ZMX-000",
            "Distance (km)": manual_distance,
            "Vehicle Type": manual_vehicle,
            "Emission Factor": factor,
            "CO₂ Emitted (kg)": emitted,
            "CO₂ Avoided (kg)": avoided
        })
        st.success("Trip added successfully!")

# Show Dashboard
if st.session_state.trip_data:
    df = pd.DataFrame(st.session_state.trip_data)
    st.subheader("📊 Dashboard Summary")
    st.dataframe(df, use_container_width=True)

    total_avoided = df["CO₂ Avoided (kg)"].sum()
    credits = round(total_avoided / 1000, 3)
    st.markdown(f"### 🌍 Total CO₂ Avoided: **{total_avoided:.2f} kg**")
    st.markdown(f"### 🪙 Zeromoto Credits Earned: **{credits} ZMT**")

    # Generate PDF Certificate
    st.subheader("📄 Download Certificate")
    if st.button("Generate Certificate"):
        cert_id = generate_unique_id()
        pdf_path = generate_certificate_pdf(
            partner=partner_name or "Unknown Partner",
            co2_kg=total_avoided,
            credits=credits,
            cert_id=cert_id
        )
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📥 Download Certificate (PDF)",
                data=f,
                file_name=f"Zeromoto_Credit_Certificate_{cert_id}.pdf",
                mime="application/pdf"
            )
else:
    st.info("Upload a trip log to see results and generate your Zeromoto Credit Certificate.")
