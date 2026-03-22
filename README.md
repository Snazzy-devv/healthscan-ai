🩺 HealthScan AI: Medical Lab Analyzer
HealthScan AI is an intelligent document processing application that transforms raw medical lab results (scans, photos, or PDFs) into structured, easy-to-understand health reports. Using State-of-the-Art OCR and LLM reasoning, it identifies biomarkers, flags potential ailments, and suggests lifestyle improvements.
✨ Key Features
 * Multi-Format Ingestion: Supports digital PDFs and raw images (JPG/PNG) via an integrated EasyOCR layer.
 * Intelligent Extraction: Automatically identifies test names, values, and reference ranges from complex tables.
 * AI Clinical Insights: Powered by GPT-4o to describe potential health status and actionable solutions.
 * Professional Export: Convert the analysis into a polished Microsoft Word (.docx) or Markdown document.
 * Privacy First: Designed to handle API keys via environment variables for secure deployment.
🏗️ Technical Stack
| Component | Technology |
|---|---|
| Frontend | Streamlit |
| OCR Engine | EasyOCR |
| PDF Parsing | PyMuPDF (fitz) |
| LLM Orchestration | LangChain |
| Intelligence | OpenAI GPT-4o |
| Document Export | python-docx |
🚀 Getting Started
1. Prerequisites
Ensure you have Python 3.9+ installed. You will also need an OpenAI API Key.
2. Installation
Clone this repository and install the dependencies:
pip install -r requirements.txt

3. Environment Setup
Create a .env file in the root directory or set your system environment variables:
OPENAI_API_KEY=your_openai_api_key_here

4. Running the App
Start the Streamlit server:
streamlit run app.py

🛠️ How it Works
 * Upload: User provides a lab result (e.g., a blood test photo).
 * OCR Processing: The system uses EasyOCR to detect text and PyMuPDF to handle digital documents.
 * Prompt Engineering: The extracted text is sent to the LLM with a specialized medical instruction set.
 * Formatting: The AI returns a Markdown-formatted analysis.
 * Export: The user can download the final report as a styled .docx file for their records.
⚠️ Disclaimer
> IMPORTANT: This application is for educational and informational purposes only. It does not provide medical diagnoses, treatments, or prescriptions. Always consult with a licensed healthcare professional before making any medical decisions based on the output of this software.
> 
📜 License
Distributed under the MIT License. See LICENSE for more information.
🩺 HealthScan AI: Medical Lab Analyzer
HealthScan AI is an intelligent document processing application that transforms raw medical lab results (scans, photos, or PDFs) into structured, easy-to-understand health reports. Using State-of-the-Art OCR and LLM reasoning, it identifies biomarkers, flags potential ailments, and suggests lifestyle improvements.
✨ Key Features
 * Multi-Format Ingestion: Supports digital PDFs and raw images (JPG/PNG) via an integrated EasyOCR layer.
 * Intelligent Extraction: Automatically identifies test names, values, and reference ranges from complex tables.
 * AI Clinical Insights: Powered by GPT-4o to describe potential health status and actionable solutions.
 * Professional Export: Convert the analysis into a polished Microsoft Word (.docx) or Markdown document.
 * Privacy First: Designed to handle API keys via environment variables for secure deployment.
🏗️ Technical Stack
| Component | Technology |
|---|---|
| Frontend | Streamlit |
| OCR Engine | EasyOCR |
| PDF Parsing | PyMuPDF (fitz) |
| LLM Orchestration | LangChain |
| Intelligence | OpenAI GPT-4o |
| Document Export | python-docx |
🚀 Getting Started
1. Prerequisites
Ensure you have Python 3.9+ installed. You will also need an OpenAI API Key.
2. Installation
Clone this repository and install the dependencies:
pip install -r requirements.txt

3. Environment Setup
Create a .env file in the root directory or set your system environment variables:
OPENAI_API_KEY=your_openai_api_key_here

4. Running the App
Start the Streamlit server:
streamlit run app.py

🛠️ How it Works
 * Upload: User provides a lab result (e.g., a blood test photo).
 * OCR Processing: The system uses EasyOCR to detect text and PyMuPDF to handle digital documents.
 * Prompt Engineering: The extracted text is sent to the LLM with a specialized medical instruction set.
 * Formatting: The AI returns a Markdown-formatted analysis.
 * Export: The user can download the final report as a styled .docx file for their records.
⚠️ Disclaimer
> IMPORTANT: This application is for educational and informational purposes only. It does not provide medical diagnoses, treatments, or prescriptions. Always consult with a licensed healthcare professional before making any medical decisions based on the output of this software.
> 
📜 License
Distributed under the MIT License. See LICENSE for more information.
