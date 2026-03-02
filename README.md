# Agentic Privacy-First Data Analyst

An agentic RAG (Retrieval-Augmented Generation) solution designed for professional statistical analysis. This tool allows you to leverage the reasoning power of Large Language Models (LLMs) without ever sending your raw, sensitive datasets to the cloud.

## 🛡️ The Privacy-First Architecture
Traditional AI data tools require uploading datasets to a third-party server. This tool uses a decoupled execution model to ensure maximum security:

* **Local Data Execution:** Your raw CSV or Excel data remains strictly on your local machine.
* **Metadata-Only Exchange:** Only column names and data types (schema) are shared with the LLM to plan the analytical approach.
* **The "Guardian" Layer:** A Python-based validation step inspects AI-generated code, corrects column typos using fuzzy matching, and ensures safety before execution.
* **Safe Insight Generation:** Only calculated numerical results (e.g., averages, trends, p-values) are sent back to the LLM for final report writing.

## 🚀 How It Works
The system follows a sophisticated two-pass agentic workflow:

1. **Intent Parsing:** The AI "Brain" identifies your request—whether it's a Run Chart, Time-Series Projection, or Descriptive Analysis.
2. **Dynamic Code Creation:** The AI writes custom Python code tailored specifically to your data's unique column structure.
3. **Execution & Capture:** Python executes the code locally, converting complex data types (like `int64` or `Timestamps`) into stable formats for reporting.
4. **Analytical Reporting:** The AI interprets the local results to produce a professional, structured Analytical Report in Markdown.



## 📋 Installation & Setup

### 1. Clone the Repository
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name

### 2. Set Up a Virtual Environment
**Windows:**
```bash
 python -m venv venv
 .\venv\Scripts\activate
```
**macOS/Linux:**
```bash
 python3 -m venv venv
 source venv/bin/activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Launch the App
```bash
streamlit run src/app.py
```
Run it in local browser (http://localhost:8501/)



