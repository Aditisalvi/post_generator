import requests
import base64
import streamlit as st
import pycountry
import base64
from io import BytesIO
from fpdf import FPDF

# Function to get all languages using pycountry
def get_all_languages():
    return sorted(
        [(language.name, language.alpha_2) for language in pycountry.languages if hasattr(language, "alpha_2")],
        key=lambda x: x[0]  # Sort by display name
    )

# Function to load Lottie animation from URL or file
def load_lottie_animation(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to download content as a file
def download_file(content, filename):
    b64 = base64.b64encode(content.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">Download {filename}</a>'
    st.markdown(href, unsafe_allow_html=True)

# Function to create a PDF file with Unicode font
def create_pdf(title, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('ArialUnicode', fname='Arial Unicode MS.ttf', uni=True)
    pdf.set_font("ArialUnicode", size=14)
    pdf.multi_cell(0, 15, title)
    pdf.ln(10)  # Add spacing
    pdf.multi_cell(0, 10, content)
    pdf_output = BytesIO()
    pdf.output(pdf_output, dest="F")  # Output PDF as binary stream
    pdf_output.seek(0)  # Reset stream position
    return pdf_output
