import random
import string

# Emission factors (kg CO₂/km)
EMISSION_FACTORS = {
    "Petrol Scooter": 0.092,
    "Diesel Car": 0.171,
    "Electric Scooter (Grid Avg)": 0.020,
    "Electric Scooter (Clean Energy)": 0.000
}

BASELINE_VEHICLE = "Petrol Scooter"
BASELINE_FACTOR = EMISSION_FACTORS[BASELINE_VEHICLE]

def calculate_emissions(distance_km, vehicle_type):
    factor = EMISSION_FACTORS.get(vehicle_type.strip())
    if factor is None:
        factor = 0.0  # fallback
    emitted = round(distance_km * factor, 3)
    avoided = round(distance_km * (BASELINE_FACTOR - factor), 3)
    return emitted, avoided, factor

def generate_unique_id(length=6):
    return "ZMT-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
