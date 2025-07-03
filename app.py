import streamlit as st
import pandas as pd
from datetime import datetime
from utils import calculate_emissions, generate_unique_id, EMISSION_FACTORS
from generate_certificate import generate_certificate_pdf

# Page config
st.set_page_config(page_title="Zeromoto Credit Tracker", layout="wide")
st.title("🪙 Zeromoto Carbon Credit Tracker")
st.caption("Track your clean kilometers, earn credits, and download your climate certificate.")

# Session state
if "trip_data" not in st.session_state:
    st.session_state.trip_data = []
if "partner_name" not in st.session_state:
    st.session_state.partner_name = ""

# Sidebar: partner name input
st.sidebar.header("Partner Information")
partner_name = st.sidebar.text_input("Partner Name / Company", value=st.session_state.partner_name)
st.session_state.partner_name = partner_name

# --- CSV Upload ---
st.header(" Upload Trip Log")
csv = st.file_uploader("CSV Format: Date, Scooter ID, Distance (km), Vehicle Type", type="csv")
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

    st.session_state.trip_data.extend(enriched)
    st.success(f"{len(enriched)} trips added from CSV.")

# --- Manual Entry ---
st.header(" Add Trip Manually")
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

# --- Dashboard ---
if st.session_state.trip_data:
    st.subheader("📊 Dashboard Summary")
    df = pd.DataFrame(st.session_state.trip_data)
    st.dataframe(df, use_container_width=True)

    total_avoided = df["CO₂ Avoided (kg)"].sum()
    total_emitted = df["CO₂ Emitted (kg)"].sum()
    credits = round(total_avoided / 1000, 3)

    st.metric("🌍 Total CO₂ Avoided", f"{total_avoided:.2f} kg")
    st.metric("🔥 Total CO₂ Emitted", f"{total_emitted:.2f} kg")
    st.metric("🪙 ZMT Credits Earned", f"{credits} ZMT")

    # --- PDF Certificate Generation ---
    st.subheader("📄 Generate Zeromoto Certificate")
    if st.button("Create PDF Certificate"):
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
    st.info("Upload a CSV or add a trip manually to begin.")

