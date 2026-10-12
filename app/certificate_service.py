from pathlib import Path
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas


OUTPUT_DIR = Path("generated")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_certificate(
    recipient_name: str,
    certificate_title: str,
    event_name: str,
    certificate_id: int,
) -> str:
    """Generate one certificate as a PDF and return its file path."""

    file_path = OUTPUT_DIR / f"certificate_{certificate_id}.pdf"

    pdf = canvas.Canvas(
        str(file_path),
        pagesize=landscape(A4),
    )

    width, height = landscape(A4)

    # Certificate border
    pdf.setLineWidth(3)
    pdf.rect(25, 25, width - 50, height - 50)

    # Certificate heading
    pdf.setFont("Helvetica-Bold", 28)
    pdf.drawCentredString(
        width / 2,
        height - 120,
        "CERTIFICATE OF ACHIEVEMENT",
    )

    # Certificate title
    pdf.setFont("Helvetica", 18)
    pdf.drawCentredString(
        width / 2,
        height - 180,
        certificate_title,
    )

    # Recipient name
    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawCentredString(
        width / 2,
        height - 245,
        recipient_name,
    )

    # Event details
    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(
        width / 2,
        height - 300,
        f"For participating in {event_name}",
    )

    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(
        width / 2,
        60,
        f"Certificate ID: {certificate_id}",
    )

    pdf.save()

    return str(file_path)