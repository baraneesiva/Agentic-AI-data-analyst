import pandas as pd

def generate_suggestions(df):
    """
    Analyzes the dataframe structure and returns a list of suggested 
    industry leading statistical softwares-style (like minitab, SPSS, etc) actions for the Streamlit UI chips.
    """
    suggestions = []
    
    if df is not None and not df.empty:
        # 1. Basic descriptive suggestion
        suggestions.append("Graphical Summary (Bar Chart, Box Plot, etc.)")
        
        # 2. Check for numerical columns for specific stats
        num_cols = df.select_dtypes(include=['number']).columns.tolist()
        if num_cols:
            suggestions.append(f"Normality Test for {num_cols[0]}")
            suggestions.append("Control Chart (Xbar-R)")
            
        # 3. Check for multiple numerical columns for correlation
        if len(num_cols) >= 2:
            suggestions.append("Correlation Matrix")
            
        # 4. Check for categorical columns for Pareto or Pie charts
        cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        if cat_cols:
            suggestions.append(f"Pareto Chart of {cat_cols[0]}")
            
    return suggestions

# NOTE: The 'categorize_intent' function has been removed. 
# Intent is now handled dynamically by call_llm() in src/core/api_handler.py 
