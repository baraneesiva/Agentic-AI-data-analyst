import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.core.api_handler import get_analysis_code, get_expert_insights, validate_llm_connection, validate_and_correct_code

st.set_page_config(layout="wide", page_title="AI Data Assistant")

if "messages" not in st.session_state: st.session_state.messages = []

# --- SIDEBAR (Settings & Upload) ---
with st.sidebar:
    st.header("Settings")
    model_provider = st.selectbox("Model Provider", ("OpenAI", "Google Gemini"))
    api_key = st.text_input("API Key", type="password")
    
    # Validation Button
    validate_btn = st.button("Validate Connection")
    if validate_btn:
        with st.spinner("Checking..."):
            is_valid, message = validate_llm_connection(model_provider, api_key)
            if is_valid: st.success(message)
            else: st.error(message)

    st.divider()
    uploaded_file = st.file_uploader("Upload Data", type=["csv", "xlsx"])

# --- MAIN APP LOGIC ---
if uploaded_file:
    if "df" not in st.session_state:
        st.session_state.df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        st.session_state.schema = {col: str(dtype) for col, dtype in st.session_state.df.dtypes.items()}
    
    df = st.session_state.df
    col_data, col_chat = st.columns([1, 2])

    with col_data: 
        st.subheader("Data Preview")
        st.dataframe(df.head(10))

    with col_chat:
        st.subheader("Analytical Conversation")
        # Render History
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if "plot" in msg: st.pyplot(msg["plot"])

        # Chat Input
        if prompt := st.chat_input("Analyze your data..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            with st.chat_message("assistant"):
                if not api_key:
                    st.error("Please provide an API Key in the sidebar.")
                else:
                    # 1. LLM Writes Code
                    with st.spinner("Generating Analysis..."):
                        raw_code = get_analysis_code(prompt, st.session_state.schema, api_key)

                    # 2. Python Validates Code
                    with st.spinner("Validating Columns..."):
                        corrected_code = validate_and_correct_code(raw_code, df.columns.tolist())
                    
                    try:
                        # 3. Python Executes Corrected Code
                        stats_results = {}
                        exec_env = {"df": df, "plt": plt, "sns": sns, "stats_results": stats_results}
                        exec(corrected_code, globals(), exec_env)
                        
                        # 4. Capture Results
                        captured_stats = exec_env.get("stats_results", {})

                        # 5. LLM Interprets Results
                        with st.spinner("Interpreting Results..."):
                            insights = get_expert_insights(prompt, captured_stats, api_key)
                        
                        # --- 6. PRESENTATION ---
                        st.markdown(insights) # Render Textual Report

                        # Render Plot
                        fig = None
                        if plt.get_fignums():
                            fig = plt.gcf()
                            st.pyplot(fig)
                        
                        # Persist
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": insights, 
                            "plot": fig if fig else None
                        })
                        if fig: plt.close(fig)

                    except Exception as e:
                        st.error(f"Analysis Error: {e}")
else:
    st.info("Please upload a file to begin.")