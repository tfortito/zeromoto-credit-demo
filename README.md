# zeromoto-credit-demo

#Zeromoto Carbon Credit Tracker (Demo App)

Zeromoto is building a platform that empowers delivery fleets and mobility partners to track, prove, and monetize their climate impact. This demo app showcases how clean kilometers from electric scooters and vehicles can be converted into measurable CO₂ savings and simulated carbon credits.

---

## Features

1. Upload trip logs via CSV  
2.Track CO₂ emitted and avoided (based on vehicle type)  
3. Earn simulated Zeromoto Credits (ZMT) like 1 credit = 1000 kg CO₂ avoided  
4. Generate and download a Carbon Credit Certificate (PDF) with a unique ID  
5. Simulate pilot fleet impact for grant and investor validation  

---

# File Structure

zeromoto-carbon-demo/
│
├── app.py ← Streamlit app entry point
├── utils.py ← Emission calculation & helper functions
├── generate_certificate.py ← PDF generator
├── requirements.txt
└── certificates/ ← Auto-generated folder for PDFs


---

#Try It Live

Hosted on [Streamlit Cloud](https://share.streamlit.io/)  




#Example CSV Format

```csv
Date,Scooter ID,Distance (km),Vehicle Type
2025-07-01,ZM-001,10.4,Electric Scooter (Grid Avg)
2025-07-01,ZM-002,7.2,Electric Scooter (Clean Energy)

Supported vehicle types:

Petrol Scooter

Diesel Car

Electric Scooter (Grid Avg)

Electric Scooter (Clean Energy)

Emission Factors Used
Vehicle Type	Emission Factor (kg CO₂/km)
Petrol Scooter (baseline)	0.092
Diesel Car	0.171
Electric Scooter (Grid Avg)	0.020
Electric Scooter (Clean)	0.000

(Source: UNFCCC CDM AMS-III.C Methodology)

 Example Certificate
After uploading a CSV, you can generate a downloadable PDF certificate with:

Partner name

Total CO₂ avoided

Credits earned

Date + unique Zeromoto ID (e.g., ZMT-2025-ABC123)

Use Cases
Grant proposals (Barcelona Activa, EIT Urban Mobility, etc.)

Verra/Gold Standard carbon credit readiness

Partner pilots for clean delivery services

Demo for investors

License
This project is open for demonstration and non-commercial use.
Contact Zeromoto for partnership, license, or deployment options.

