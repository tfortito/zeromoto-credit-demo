from fpdf import FPDF
from datetime import datetime
import os

def generate_certificate_pdf(partner, co2_kg, credits, cert_id):
    # 🛡️ Quick fix: remove Unicode characters that cause PDF export errors
    partner = partner.encode("ascii", errors="ignore").decode()

    # File setup
    today = datetime.today().strftime("%Y-%m-%d")
    filename = f"{cert_id}_Zeromoto_Certificate.pdf"
    folder = "certificates"
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)

    # PDF creation
    pdf = FPDF("L", "mm", "A4")
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)

    # Title
    pdf.cell(0, 15, "Zeromoto Carbon Credit Certificate", ln=True, align="C")

    # Certificate body
    pdf.set_font("Arial", "", 16)
    pdf.ln(10)
    pdf.cell(0, 12, f"Issued to: {partner}", ln=True, align="C")
    pdf.cell(0, 12, f"Certificate ID: {cert_id}", ln=True, align="C")
    pdf.cell(0, 12, f"Issue Date: {today}", ln=True, align="C")
    pdf.cell(0, 12, f"Total CO₂ Avoided: {co2_kg:.2f} kg", ln=True, align="C")
    pdf.cell(0, 12, f"ZMT Credits Earned: {credits:.3f}", ln=True, align="C")

    # Footer
    pdf.ln(15)
    pdf.set_font("Arial", "I", 12)
    pdf.cell(0, 10, "This certificate simulates climate impact for clean mobility fleets.", ln=True, align="C")

    # Output
    pdf.output(filepath)
    return filepath
