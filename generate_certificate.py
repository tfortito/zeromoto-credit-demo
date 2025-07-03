from fpdf import FPDF
from datetime import datetime
import os

def generate_certificate_pdf(partner, co2_kg, credits, cert_id):
    today = datetime.today().strftime("%Y-%m-%d")
    filename = f"{cert_id}_Zeromoto_Certificate.pdf"
    filepath = os.path.join("certificates", filename)

    # Create directory if it doesn't exist
    os.makedirs("certificates", exist_ok=True)

    pdf = FPDF("L", "mm", "A4")
    pdf.add_page()
    pdf.set_font("Arial", "B", 24)

    # Title
    pdf.cell(0, 20, "Zeromoto Carbon Credit Certificate", ln=True, align="C")

    # Partner Name
    pdf.set_font("Arial", "", 18)
    pdf.cell(0, 15, f"Issued to: {partner}", ln=True, align="C")

    # Details
    pdf.ln(10)
    pdf.set_font("Arial", "", 14)
    pdf.cell(0, 10, f"Certificate ID: {cert_id}", ln=True, align="C")
    pdf.cell(0, 10, f"Date Issued: {today}", ln=True, align="C")
    pdf.cell(0, 10, f"Total CO₂ Avoided: {co2_kg:.2f} kg", ln=True, align="C")
    pdf.cell(0, 10, f"Zeromoto Credits Earned: {credits:.3f} ZMT", ln=True, align="C")

    # Footer
    pdf.ln(20)
    pdf.set_font("Arial", "I", 12)
    pdf.cell(0, 10, "This certificate is a simulated climate impact report issued by Zeromoto.", ln=True, align="C")

    pdf.output(filepath)
    return filepath
