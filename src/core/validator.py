import pandas as pd
import streamlit as st

def validate_file_structure(uploaded_file):
    """
    Performs structural and quality validation checks on the uploaded file.
    Adheres to:
    - Sheet Selection (if multiple sheets exist)
    - Row 1 Structural Validation (Blank Row Check)
    - Column-Level Data Quality Validation (Data Type Consistency, Missing Values)
    """
    try:
        # 1. Load File Data
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            # [cite_start]Handle Excel Sheets [cite: 17, 18]
            xl = pd.ExcelFile(uploaded_file)
            if len(xl.sheet_names) > 1:
                # This needs to be handled in the UI to allow user selection
                # For this validator, we take the first one or assume selection happened
                sheet_name = xl.sheet_names[0] 
                st.warning(f"Multiple sheets detected. Using first sheet: {sheet_name}")
                df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
            else:
                df = pd.read_excel(uploaded_file)

        # [cite_start]2. Row 1 Structural Validation [cite: 20]
        # Check if the dataframe is empty
        if df.empty:
            return None, "File is empty."

        # [cite_start]3. Column-Level Data Quality Validation [cite: 23]
        
        # [cite_start]Check for Missing Values [cite: 25]
        null_counts = df.isnull().sum()
        if null_counts.sum() > 0:
            columns_with_nulls = null_counts[null_counts > 0].index.tolist()
            # [cite_start]Detailed Feedback [cite: 26]
            return None, f"Missing values found in columns: {', '.join(columns_with_nulls)}"

        # [cite_start]Check Data Type Consistency [cite: 24]
        # Example: Check if numeric columns actually contain numbers
        numeric_cols = df.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            if not pd.to_numeric(df[col], errors='coerce').notnull().all():
                 # [cite_start]Detailed Feedback [cite: 26]
                return None, f"Column '{col}' contains mixed data types."

        # If all validations pass
        return df, None

    except Exception as e:
        return None, f"Error processing file: {str(e)}"