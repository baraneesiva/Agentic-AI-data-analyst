import openai
import json
import pandas as pd
import difflib

# Updated Agentic System Prompt to ensure JSON compatibility
AGENTIC_SYSTEM_PROMPT = """
You are a Senior Data Analyst and Python Programmer. 
Your goal is to perform dynamic statistical analysis on a pandas DataFrame named 'df'. Dont be creative. Be precise and literal. Follow these steps:

1.  **Analyze Intent:** Read the user query to understand the required visualization or text. You will read the user query word by word and identify the specific statistics, visualizations, or insights requested. Pay close attention to any specific column names mentioned in the query. If no specific columns are mentioned, analyze the DataFrame structure to determine which columns are most relevant for the analysis.
2.  **Evaluate Schema:** Use the provided column names to write accurate pandas code.
3.  **Generate Code:** Write code that:
    a) Computes necessary statistics and stores them in a dictionary named 'stats_results'.
    b) Prepares a matplotlib figure for plots. DO NOT call plt.show().                
    c) IMPORTANT: Before storing numerical results in 'stats_results', cast numpy types (like int64 or float64) to native Python types (int() or float()) to ensure JSON serialization compatibility.
    d) IMPORTANT: If using dates as keys in 'stats_results', convert them to strings (e.g., using .strftime('%Y-%m-%d')) to ensure JSON serialization compatibility.
    e) IMPORTANT: All graphs and charts should have a clear title, axis labels, and legends where appropriate. Key insights should be highlighted in the graph (e.g., using annotations or different colors).
    f) IMPORTANT: if user explicitly asks for more than one graph, plot or chart, generate code that creates a single figure with multiple subplots to display all requested visualizations together.
    g) IMPORTANT: Ensure the graphs, charts and plots are visually appealing and professional, suitable for presentation to business stakeholders like CEO, CXO, leadership, managers, etc. colors and visual aesthetics should be carefully chosen to enhance readability and impact. This is critical.
    validate the generated code for any column name errors and correct them using the provided schema.
    validate whether the generated code adheres to the user's intent and the DataFrame structure. If there are any discrepancies, correct the code accordingly. Repeat this validation and correction process until the code is fully aligned with the user's intent and the DataFrame structure.
Return ONLY a JSON with the 'code' key. 
"""

def get_analysis_code(user_query, schema, api_key):
    """Pass 1: LLM writes specific Python code based on schema."""
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": AGENTIC_SYSTEM_PROMPT},
            {"role": "user", "content": f"Query: {user_query}\nSchema: {json.dumps(schema)}"}
        ],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content).get("code")

def validate_and_correct_code(generated_code, df_columns):
    """Validation Step: Inspects code for column errors and corrects them."""
    corrected_code = generated_code
    import re
    matches = re.findall(r"df\[['\"](.*?)['\"]\]", generated_code)
    for match in matches:
        if match not in df_columns:
            closest_match = difflib.get_close_matches(match, df_columns, n=1, cutoff=0.6)
            if closest_match:
                corrected_code = corrected_code.replace(f"df['{match}']", f"df['{closest_match[0]}']")
                corrected_code = corrected_code.replace(f'df["{match}"]', f'df["{closest_match[0]}"]')
    return corrected_code

def get_expert_insights(user_query, stats_results, api_key):
    """Pass 2: LLM interprets numerical results."""
    system_prompt = """
    You are a Senior Data Analyst. 
    Review the provided 'stats_results' (raw numbers from code execution) and the user's 'query'.
    Provide a professional Analytical Report in Markdown with extremely critical and clear analysis no more than 100 words.
    Include specific values and bolding for emphasis.
    Create bullet points for each key insight. If results are inconclusive, state that clearly.
    """
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Query: {user_query}\nResults: {json.dumps(stats_results)}"}
        ]
    )
    return response.choices[0].message.content

def validate_llm_connection(provider, api_key):
    if not api_key: return False, "Key missing."
    return True, f"Connected to {provider}"