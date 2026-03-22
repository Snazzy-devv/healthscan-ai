import streamlit as st
import fitz  # PyMuPDF
import easyocr
import numpy as np
import io
import os
from PIL import Image
from docx import Document
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

load_dotenv(override=True)

# Set OpenRouter API Key & Base URL
os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"

# Instantiate OpenAI client
ai_client = OpenAI(
    base_url=BASE_URL,
    api_key=os.environ.get("OPENROUTER_API_KEY")
)

# 1. SETUP & CONFIGURATION
# This pulls the key from your environment/system secrets automatically
os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(page_title="HealthScan AI", page_icon="💊", layout="centered")

# Initialize OCR (Loads once)
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])

reader = load_ocr()

# --- 2. DOCUMENT PROCESSING FUNCTIONS ---

def extract_text(uploaded_file):
    """Handles both PDF and Image OCR"""
    file_type = uploaded_file.type
    text = ""
    
    if "pdf" in file_type:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text()
    else:
        # OCR for JPG/PNG
        image = Image.open(uploaded_file)
        img_np = np.array(image)
        results = reader.readtext(img_np, detail=0)
        text = " ".join(results)
    return text

def create_docx(markdown_content):
    """Converts AI Markdown into a Professional Word Document"""
    doc = Document()
    doc.add_heading('Medical Lab Analysis Report', 0)
    
    for line in markdown_content.split('\n'):
        if line.startswith('## '):
            doc.add_heading(line.replace('## ', ''), level=1)
        elif line.startswith('### '):
            doc.add_heading(line.replace('### ', ''), level=2)
        elif line.startswith('* '):
            doc.add_paragraph(line.replace('* ', ''), style='List Bullet')
        elif line.strip():
            doc.add_paragraph(line)
            
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- 3. THE USER INTERFACE ---

st.title("🩺 HealthScan AI")
st.subheader("Instant Lab Result Analysis & Document Converter")
st.markdown("---")

uploaded_file = st.file_uploader("Upload a photo or PDF of your lab results", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file:
    with st.status("Analyzing your document...", expanded=True) as status:
        st.write("Reading text from file...")
        raw_text = extract_text(uploaded_file)
        
        st.write("Consulting AI Medical Knowledge Base...")
        llm = ChatOpenAI(model="gpt-4o") # No key needed here, it's in the environment
        
        system_prompt = SystemMessage(content="""
            You are a Medical Analyst. You receive raw text from lab scans.
            Analyze the biomarkers and generate a report in Markdown.
            
            Structure:
            ## 📋 Summary
            ## 🧪 Lab Results Table (Test, Result, Range, Status)
            ## ⚠️ Detected Ailments/Issues
            ## 💡 Solutions & Advice
            - **Medications/Supplements:** (General advice)
            - **Avoid:** (Foods/Activities)
            - **Improvement:** (Lifestyle changes)
            
            DISCLAIMER: State clearly that this is not a clinical diagnosis.
        """)
        
        user_prompt = HumanMessage(content=f"Analyze this content:\n\n{raw_text}")
        response = llm.invoke([system_prompt, user_prompt])
        report_md = response.content
        
        status.update(label="Analysis Complete!", state="complete", expanded=False)

    # Display Analysis
    st.markdown(report_md)
    
    # Export Options
    st.markdown("---")
    st.subheader("📥 Download Your Report")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Export as .doc
        docx_data = create_docx(report_md)
        st.download_button(
            label="Download as Word (.docx)",
            data=docx_data,
            file_name="Medical_Analysis.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
    with col2:
        # Export as .pdf (formatted via Markdown)
        st.download_button(
            label="Download as Text/PDF (.md)",
            data=report_md,
            file_name="Medical_Analysis.md",
            mime="text/markdown"
        )

else:
    st.info("Please upload a file to begin.")

