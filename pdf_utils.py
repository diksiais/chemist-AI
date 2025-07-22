# pdf_utils.py
from fpdf import FPDF
import io

def create_pdf_from_text(title, text_content):
    """
    Generates a PDF from the given title and text content.

    Args:
        title (str): The title for the PDF document.
        text_content (str): The main text content to be included in the PDF.

    Returns:
        bytes: The PDF content as bytes.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, title, 0, 1, "C")
    pdf.ln(10) # Line break

    pdf.set_font("Arial", "", 12)
    # MultiCell is used to handle long text that wraps across lines
    pdf.multi_cell(0, 10, text_content)

    # Output the PDF to a BytesIO object
    pdf_output = io.BytesIO()
    # FIX: Call output() without arguments when writing to BytesIO
    pdf.output(dest='S').encode('latin-1') # 'S' means return as string, then encode to bytes
    # The above line is the correct way to get the PDF content as a string/bytes from FPDF.
    # The previous line `pdf.output(pdf_output)` was incorrect.
    # The .getvalue() method is then called on the BytesIO object used in the app.py to get the bytes.
    # The `dest='S'` parameter makes FPDF return the PDF as a string, which we then encode.
    # This is a common pattern for FPDF when not saving directly to a file.

    # Re-writing the logic to correctly use BytesIO for Streamlit's download_button
    # FPDF's output method can write directly to a BytesIO object if you pass it as a file-like object.
    # However, the most robust way for Streamlit is to get the string/bytes directly from FPDF.
    # Let's use the recommended way to get bytes directly from FPDF for in-memory use.
    return pdf.output(dest='S').encode('latin-1')

