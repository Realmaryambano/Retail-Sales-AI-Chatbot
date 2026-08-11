import streamlit as st
import pandas as pd
from google import genai

# Page Configuration
st.set_page_config(page_title="Retail Sales AI Assistant", page_icon="📊", layout="wide")

st.title("📊 Retail Sales AI Chatbot")
st.markdown("Ask questions in plain English about your 198,808 sales records.")

# 1. Load the local Excel dataset
@st.cache_data
def load_data():
    file_path = "01-Aug-26 to 10-Aug-26.xlsx"
    return pd.read_excel(file_path)

try:
    df = load_data()
    st.success(f"Dataset loaded successfully! Total Rows: {len(df):,}")
except Exception as e:
    st.error(f"Error loading file: {e}")
    st.stop()

# 2. API Key Input
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter your Google Gemini API Key", type="password")

if not api_key:
    st.warning("Please enter your free Google Gemini API key in the sidebar to start chatting.")
    st.stop()

# Initialize Gemini Client
client = genai.Client(api_key=api_key)

# 3. User Chat Interface
user_query = st.text_input("Ask a question (e.g., 'What is the total net sale for Hob Ocean Mall?'):")

if user_query:
    with st.spinner("Analyzing data..."):
        try:
            # We provide a data sample and schema context to Gemini so it writes the correct analysis logic
            prompt = f"""
            You are an expert data analyst. You have a pandas DataFrame named `df` containing retail sales data with the following columns:
            {list(df.columns)}
            
            Sample rows:
            {df.head(3).to_string()}
            
            The user wants to answer this question: "{user_query}"
            
            Write executable Python code using pandas on `df` to get the answer. Store the final result in a variable named `result`. 
            Return ONLY valid Python code block inside ```python ... ``` without any markdown errors, so it can be executed.
            """
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            
            # Extract code from response
            raw_text = response.text
            if "```python" in raw_text:
                code_block = raw_text.split("```python")[1].split("```")[0].strip()
            elif "```" in raw_text:
                code_block = raw_text.split("```")[1].split("```")[0].strip()
            else:
                code_block = raw_text.strip()
                
            # Execute the generated python code securely on our dataframe
            local_vars = {"df": df, "pd": pd}
            exec(code_block, {}, local_vars)
            
            final_answer = local_vars.get("result", "Analysis completed, but no 'result' variable was returned.")
            
            st.markdown("### Answer:")
            st.write(final_answer)
            
        except Exception as e:
            st.error(f"An error occurred during analysis: {e}")