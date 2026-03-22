import streamlit as st
import pdfplumber  
import easyocr
import numpy as np
import io
import os
from PIL import Image
from docx import Document
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# Load environment variables
load_dotenv()

# Streamlit page config
st.set_page_config(page_title="HealthScan AI", page_icon="💊", layout="centered")

# --- LOAD OCR MODEL ---
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])

reader = load_ocr()

# --- TEXT EXTRACTION FUNCTION ---
def extract_text(uploaded_file):
    text = ""

    # Handle PDF
    if "pdf" in uploaded_file.type:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

    # Handle Images
    else:
        image = Image.open(uploaded_file)
        img_np = np.array(image)
        results = reader.readtext(img_np, detail=0)
        text = " ".join(results)

    return text


# --- DOCX CREATION FUNCTION ---
def create_docx(markdown_content):
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


# --- UI ---
st.title("🩺 HealthScan AI")
st.subheader("Instant Lab Result Analysis & Document Converter")
st.markdown("---")

uploaded_file = st.file_uploader(
    "Upload a photo or PDF of your lab results",
    type=["pdf", "png", "jpg", "jpeg"]
)

if uploaded_file:
    with st.status("Analyzing your document...", expanded=True) as status:

        st.write("📄 Reading text from file...")
        raw_text = extract_text(uploaded_file)

        if not raw_text.strip():
            st.error("❌ Could not extract text from the file.")
            st.stop()

        st.write("🤖 Consulting AI Medical Knowledge Base...")

        # Initialize LLM
        llm = ChatOpenAI(
            model="gpt-4o",
            api_key=os.getenv("OPENAI_API_KEY")  # ✅ Use Streamlit secrets
        )

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

DISCLAIMER: This is not a clinical diagnosis.
        """)

        user_prompt = HumanMessage(
            content=f"Analyze this content:\n\n{raw_text}"
        )

        try:
            response = llm.invoke([system_prompt, user_prompt])
            report_md = response.content
        except Exception as e:
            st.error(f"❌ AI Error: {e}")
            st.stop()

        status.update(label="✅ Analysis Complete!", state="complete", expanded=False)

    # --- DISPLAY RESULT ---
    st.markdown(report_md)

    # --- DOWNLOAD OPTIONS ---
    st.markdown("---")
    st.subheader("📥 Download Your Report")

    col1, col2 = st.columns(2)

    with col1:
        docx_data = create_docx(report_md)
        st.download_button(
            label="Download as Word (.docx)",
            data=docx_data,
            file_name="Medical_Analysis.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    with col2:
        st.download_button(
            label="Download as Markdown (.md)",
            data=report_md,
            file_name="Medical_Analysis.md",
            mime="text/markdown"
        )

else:
    st.info("📤 Please upload a file to begin.")
