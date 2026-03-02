# Agentic Privacy-First Data Analyst

An agentic RAG (Retrieval-Augmented Generation) solution for performing professional statistical analysis without ever sending your raw data to an LLM.

## 🛡️ The Privacy-First Advantage
Traditional AI data tools require you to upload your datasets to the cloud. This tool changes the paradigm:
* **Local Data Execution:** Your raw CSV/Excel data stays on your machine.
* **Metadata-Only Exchange:** Only column names (schema) are sent to the AI to plan the analysis.
* **Local Validation:** A Python-based "Guardian" layer validates AI-generated code against your local data before execution.
* **Safe Insights:** Only calculated results (not raw rows) are shared back for final report generation.

## 🚀 How It Works
1. **Analyze Intent:** The AI "Brain" parses your natural language request (e.g., "Create a run chart for revenue").
2. **Code Generation:** The AI writes specific Python instructions based on your data map.
3. **Python Validation:** The system checks the code for errors and corrects column typos locally.
4. **Local Execution:** Python runs the math and generates charts behind your firewall.
5. **Analytical Reporting:** The AI interprets the results and writes a professional report.

## 🛠️ Tech Stack
* **Orchestration:** OpenAI GPT-4o / Google Gemini.
* **Interface:** Streamlit.
* **Data Engine:** Pandas, Scipy, Matplotlib.

## 📋 Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
