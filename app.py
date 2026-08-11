import streamlit as st
import pandas as pd
import glob
import os
from google import genai

# ──────────────────────────────────────────────────────────────────────────
# 1. PAGE CONFIGURATION & METADATA SETUP
# ──────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Assistant | Retail Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────
# 2. PROFESSIONAL DESIGN SYSTEM & CORPORATE BLUE CSS
# ──────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg-main: #090d16;        /* Deep matte corporate blue background */
    --bg-card: #111827;        /* Clean card surface */
    --text-main: #f3f4f6;      /* Off-white primary text */
    --text-muted: #9ca3af;     /* Soft slate gray secondary text */
    --primary: #2563eb;        /* Professional Enterprise Blue */
    --primary-hover: #1d4ed8;  /* Deeper blue for interactive states */
    --border-color: #1f2937;   /* Subtle container borders */
}

html, body, [class*="css"] { 
    font-family: 'Inter', sans-serif !important; 
}

.stApp {
    background-color: var(--bg-main);
    color: var(--text-main);
}

#MainMenu {visibility: hidden;} 
footer {visibility: hidden;} 
header[data-testid="stHeader"] {background: transparent;}

/* Masthead Styling */
.masthead { padding: 4px 0 0 0; }
.masthead .eyebrow {
    font-size: 0.75rem; 
    letter-spacing: 0.15em;
    text-transform: uppercase; 
    color: #60a5fa; 
    margin: 0 0 4px 0; 
    font-weight: 600;
}
.masthead h1 {
    font-weight: 700;
    font-size: 2.2rem; 
    color: var(--text-main);
    margin: 0;
    letter-spacing: -0.01em;
}
.masthead p.sub {
    color: var(--text-muted); 
    font-size: 0.95rem;
    margin: 6px 0 0 0; 
}
.blue-divider {
    height: 1px; 
    margin: 20px 0;
    background: var(--border-color);
    border: none;
}

/* Sidebar Console Styling */
section[data-testid="stSidebar"] {
    background-color: #05080f; 
    border-right: 1px solid var(--border-color);
}
section[data-testid="stSidebar"] * { color: var(--text-main) !important; }
section[data-testid="stSidebar"] .console-eyebrow {
    font-size: 0.7rem; 
    letter-spacing: 0.12em;
    text-transform: uppercase; 
    color: #60a5fa !important; 
    margin-bottom: 2px;
}
section[data-testid="stSidebar"] h3 {
    font-weight: 600; 
    font-size: 1.1rem; 
    margin: 0 0 4px 0;
}
section[data-testid="stSidebar"] hr { border-color: var(--border-color); }
section[data-testid="stSidebar"] .stTextInput input {
    background: #0f172a !important; 
    border: 1px solid var(--border-color) !important;
    border-radius: 6px !important; 
    color: var(--text-main) !important;
}
section[data-testid="stSidebar"] [data-testid="stFormSubmitButton"] button {
    width: 100%; 
    background: var(--primary) !important; 
    color: #ffffff !important;
    border: none !important; 
    border-radius: 6px !important; 
    font-weight: 600 !important;
    padding: 0.5rem 0 !important; 
}
section[data-testid="stSidebar"] [data-testid="stFormSubmitButton"] button:hover {
    background: var(--primary-hover) !important;
}

/* Status Badges */
.status-pill {
    display: inline-flex; align-items: center; gap: 6px; 
    font-size: 0.75rem; padding: 4px 10px; border-radius: 999px; margin-top: 4px;
}
.status-pill.on { background: rgba(37, 99, 235, 0.15); border: 1px solid var(--primary); }
.status-pill.off { background: rgba(156, 163, 175, 0.1); border: 1px solid var(--border-color); }
.status-dot { width: 6px; height: 6px; border-radius: 50%; }
.status-dot.on { background: #60a5fa; }
.status-dot.off { background: #9ca3af; }

/* KPI Top Metric Cards Grid */
.kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 20px; }
.kpi-card {
    background: var(--bg-card); 
    border: 1px solid var(--border-color); 
    border-top: 3px solid var(--primary);
    border-radius: 6px; 
    padding: 14px 16px;
}
.kpi-card .k-label {
    font-size: 0.7rem; letter-spacing: 0.08em;
    text-transform: uppercase; color: var(--text-muted);
}
.kpi-card .k-value {
    font-weight: 700; font-size: 1.45rem; 
    color: var(--text-main); margin-top: 4px;
}

/* Quick Action Buttons */
div[data-testid="stButton"] button {
    background: var(--bg-card) !important; 
    color: var(--text-main) !important;
    border: 1px solid var(--border-color) !important; 
    border-bottom: 2px solid var(--primary) !important;
    border-radius: 6px !important; 
    font-weight: 500 !important; 
    font-size: 0.82rem !important; 
    padding: 0.5rem !important;
}
div[data-testid="stButton"] button:hover {
    background: var(--primary) !important; 
    color: #ffffff !important; 
    border-color: var(--primary) !important;
}

/* Section Labels & Chat Containers */
.section-label {
    font-size: 0.72rem; letter-spacing: 0.1em;
    text-transform: uppercase; color: var(--text-muted); margin: 6px 0 8px 2px;
}
[data-testid="stChatMessage"] {
    background: var(--bg-card); 
    border: 1px solid var(--border-color); 
    border-radius: 8px;
    padding: 8px 12px; 
    margin-bottom: 10px;
}
div[data-testid="stChatInput"] textarea {
    background: #0f172a !important; 
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important; 
    color: var(--text-main) !important;
}

/* Computed Scalar Result Highlight Card */
.answer-figure {
    background: #0f172a; 
    color: var(--text-main); 
    border: 1px solid var(--primary);
    border-radius: 8px; 
    padding: 14px 18px; 
    margin-top: 4px;
}
.answer-figure .a-label {
    font-size: 0.7rem; letter-spacing: 0.1em;
    text-transform: uppercase; color: #60a5fa;
}
.answer-figure .a-value {
    font-weight: 700; font-size: 1.75rem; margin-top: 2px;
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# 3. HEADER / MASTHEAD SECTION (plain language, no jargon)
# ──────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="masthead">
    <p class="eyebrow">Sales Assistant</p>
    <h1>Store Sales Dashboard</h1>
    <p class="sub">Ask a question in plain words and get an instant answer from your sales data.</p>
</div>
<hr class="blue-divider">
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# 4. DATA LOADING LAYER (CACHED, auto-detects the Excel file)
# ──────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    # Try the exact expected name first, then fall back to any .xlsx file
    # sitting next to this script — avoids breakage from small filename
    # differences (spaces vs underscores, date range changes, etc.)
    candidates = [
        "testing - Copy.xlsx",
        
    ]
    for name in candidates:
        if os.path.exists(name):
            return pd.read_excel(name)

    xlsx_files = glob.glob("*.xlsx")
    if xlsx_files:
        return pd.read_excel(xlsx_files[0])

    raise FileNotFoundError("No sales Excel file found in the app folder.")

try:
    df = load_data()
except Exception:
    st.error("⚠️ We couldn't find the sales data file. Please make sure the Excel file is placed in the same folder as this app, then refresh the page.")
    st.stop()

# ──────────────────────────────────────────────────────────────────────────
# 5. SIDEBAR ACCESS CONSOLE & AUTHENTICATION (plain language)
# ──────────────────────────────────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "gemini_key" not in st.session_state:
    st.session_state.gemini_key = ""

with st.sidebar:
    st.markdown('<p class="console-eyebrow">Setup</p>', unsafe_allow_html=True)
    st.markdown("### Connect the Assistant")
    st.caption("Paste your API key once below to switch the assistant on.")

    with st.form("auth_form", clear_on_submit=False):
        key_input = st.text_input(
            "API Key",
            type="password",
            placeholder="Paste your key here",
            value=st.session_state.gemini_key,
        )
        connect_clicked = st.form_submit_button("Turn On Assistant →")

    if connect_clicked:
        if key_input.strip():
            st.session_state.gemini_key = key_input.strip()
            st.session_state.authenticated = True
        else:
            st.session_state.authenticated = False

    if st.session_state.authenticated:
        st.markdown(
            '<span class="status-pill on"><span class="status-dot on"></span>Assistant is On</span>',
            unsafe_allow_html=True,
        )
        if st.button("Turn Off", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.gemini_key = ""
            st.session_state.messages = []
            st.rerun()
    else:
        st.markdown(
            '<span class="status-pill off"><span class="status-dot off"></span>Assistant is Off</span>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown('<p class="console-eyebrow">Data Snapshot</p>', unsafe_allow_html=True)
    st.markdown(f"**{len(df):,}** sales entries")
    if "Store_Name" in df.columns:
        st.markdown(f"**{df['Store_Name'].nunique():,}** stores")
    if "Transact_Date" in df.columns:
        try:
            dmin = pd.to_datetime(df["Transact_Date"]).min().strftime("%d %b")
            dmax = pd.to_datetime(df["Transact_Date"]).max().strftime("%d %b %Y")
            st.markdown(f"**Covers:** {dmin} – {dmax}")
        except Exception:
            pass

if not st.session_state.authenticated:
    st.warning("🔒 To get started, paste your API key in the box on the left and press **Turn On Assistant**.")
    st.stop()

# Initialize Gemini Client using official SDK
client = genai.Client(api_key=st.session_state.gemini_key)

# ──────────────────────────────────────────────────────────────────────────
# 6. EXECUTIVE KPI METRICS STRIP (PKR currency, plain labels)
# ──────────────────────────────────────────────────────────────────────────
total_revenue = df["Net_Sale"].sum() if "Net_Sale" in df.columns else None
total_qty = df["Quantity"].sum() if "Quantity" in df.columns else None
n_stores = df["Store_Name"].nunique() if "Store_Name" in df.columns else None
n_invoices = df["Invoice_No"].nunique() if "Invoice_No" in df.columns else None

kpi_html = '<div class="kpi-row">'
kpi_html += f'<div class="kpi-card"><div class="k-label">Total Sales</div><div class="k-value">Rs {total_revenue:,.0f}</div></div>' if total_revenue is not None else ""
kpi_html += f'<div class="kpi-card"><div class="k-label">Items Sold</div><div class="k-value">{total_qty:,.0f}</div></div>' if total_qty is not None else ""
kpi_html += f'<div class="kpi-card"><div class="k-label">Total Bills</div><div class="k-value">{n_invoices:,}</div></div>' if n_invoices is not None else ""
kpi_html += f'<div class="kpi-card"><div class="k-label">Stores</div><div class="k-value">{n_stores:,}</div></div>' if n_stores is not None else ""
kpi_html += '</div>'
st.markdown(kpi_html, unsafe_allow_html=True)
st.caption("Note: these totals include returns/refunds, which show up as negative amounts.")

# ──────────────────────────────────────────────────────────────────────────
# 7. QUICK-ACTION QUERY SHORTCUTS (plain, everyday wording)
# ──────────────────────────────────────────────────────────────────────────
if "active_query" not in st.session_state:
    st.session_state.active_query = None
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown('<p class="section-label">Quick Questions — Just Click One</p>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🏢 Top 5 Stores by Sales", use_container_width=True):
        st.session_state.active_query = "Which 5 stores made the most total sales?"
with col2:
    if st.button("🏷️ Best-Selling Categories", use_container_width=True):
        st.session_state.active_query = "Which 5 product categories sold the most pieces?"
with col3:
    if st.button("💵 Total Sales So Far", use_container_width=True):
        st.session_state.active_query = "What is the total sales amount, in PKR, across all stores?"
with col4:
    if st.button("📅 Sales by Day", use_container_width=True):
        st.session_state.active_query = "Show me the total sales for each day."

st.markdown('<hr class="blue-divider" style="margin:16px 0;">', unsafe_allow_html=True)
st.markdown('<p class="section-label">Ask Your Own Question</p>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────
# 8. PERSISTENT CONVERSATION HISTORY DISPLAY
# ──────────────────────────────────────────────────────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("is_figure"):
            st.markdown(
                f'<div class="answer-figure"><div class="a-label">Answer</div>'
                f'<div class="a-value">{message["content"]}</div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(message["content"])

user_query = st.chat_input('Type a question, like "Which store sold the most on 5 August?"')

if st.session_state.active_query:
    user_query = st.session_state.active_query
    st.session_state.active_query = None

# ──────────────────────────────────────────────────────────────────────────
# 9. AI AGENT REASONING & EXECUTION ENGINE (EXACT MATCHING & RESILIENT)
# ──────────────────────────────────────────────────────────────────────────
if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Looking into it…"):
            try:
                # --- PRE-PROCESSING NORMALIZATION ---
                df['Transact_Date'] = pd.to_datetime(df['Transact_Date'])

                # Create clean lookup versions of store names (fixes case,
                # extra spaces, and hidden characters like non-breaking spaces)
                df['Store_Name_Clean'] = (
                    df['Store_Name'].astype(str)
                    .str.upper()
                    .str.replace('\xa0', ' ', regex=False)
                    .str.replace(r'\s+', ' ', regex=True)
                    .str.strip()
                )

                prompt = f"""
                You are a retail data analyst. You have a pandas DataFrame named `df` with sales data
                from stores in Pakistan. All money values are in PKR (Pakistani Rupees) — never treat
                them as US dollars or any other currency, and never convert them.

                The columns are: {list(df.columns)}

                IMPORTANT DATA FACTS:
                - `Net_Sale` is the actual amount received in PKR, after discounts. Use this for "sales"
                  or "revenue" questions unless the user clearly asks for something else (like gross
                  amount or discount).
                - Some rows have NEGATIVE Quantity and Net_Sale — these are returns/refunds, not errors.
                  Include them in totals by default (a store's true net sales already accounts for
                  returns). Only exclude them if the user specifically asks to ignore returns/refunds.
                - `Store_Name_Clean` is an uppercase, whitespace-cleaned version of `Store_Name`. Always
                  filter on `Store_Name_Clean`, not the raw `Store_Name` column.
                - The user may write store names, product names, or dates with typos, shorthand,
                  abbreviations, or in Roman Urdu/English mix. Do your best to match their intent to the
                  closest real value in the data.
                - If the user names one specific, exact store (e.g. "HOB LUCKY 1 MALL"), match it
                  EXACTLY using `df['Store_Name_Clean'] == 'HOB LUCKY 1 MALL'`. Do NOT use `.contains()`
                  for a specific store name, because similar-sounding stores/kiosks (e.g. "LUCKY 1
                  (KIOSK)") are separate locations and must not be mixed together.
                - Only use `.contains(...)` style partial matching when the user's request is broad or
                  clearly asks to include multiple related stores.
                - 'Transact_Date' is already a proper date column.

                Sample data rows:
                {df[['Transact_Date', 'Store_Name', 'Net_Sale', 'Quantity']].head(3).to_string()}

                User's question: "{user_query}"

                Write clean, executable Python code using pandas on `df` to answer this question.
                Store the final answer (a number, a short table, or a short piece of text) in a variable
                named `result`. Keep any numeric result as a plain number (no currency symbols or commas
                inside it) — formatting for display is handled separately.
                Return ONLY a Python code block inside ```python ... ``` with no extra explanation.
                """

                response = client.models.generate_content(
                    model='gemini-3.5-flash',
                    contents=prompt
                )

                raw_text = response.text
                if "```python" in raw_text:
                    code_block = raw_text.split("```python")[1].split("```")[0].strip()
                elif "```" in raw_text:
                    code_block = raw_text.split("```")[1].split("```")[0].strip()
                else:
                    code_block = raw_text.strip()

                local_vars = {"df": df, "pd": pd}
                exec(code_block, {}, local_vars)

                result = local_vars.get("result", None)

                if result is None:
                    final_text = "I looked into that, but I couldn't come up with a clear answer. Could you try rephrasing your question?"
                    st.markdown(final_text)
                    st.session_state.messages.append({"role": "assistant", "content": final_text})
                elif isinstance(result, (pd.DataFrame, pd.Series)):
                    display_df = result.to_frame() if isinstance(result, pd.Series) else result
                    st.dataframe(display_df, use_container_width=True)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": display_df.to_markdown() if hasattr(display_df, "to_markdown") else str(display_df),
                    })
                elif isinstance(result, (int, float)):
                    # Money-related results tend to be floats (Net_Sale, Gross_Amount, etc.)
                    # while simple counts (quantity, number of bills/stores) are ints.
                    if isinstance(result, float):
                        formatted = f"Rs {result:,.0f}"
                    else:
                        formatted = f"{result:,}"
                    st.markdown(
                        f'<div class="answer-figure"><div class="a-label">Answer</div>'
                        f'<div class="a-value">{formatted}</div></div>',
                        unsafe_allow_html=True,
                    )
                    st.session_state.messages.append({"role": "assistant", "content": formatted, "is_figure": True})
                else:
                    st.markdown(str(result))
                    st.session_state.messages.append({"role": "assistant", "content": str(result)})

            except Exception as e:
                friendly_msg = "Sorry, I couldn't work that out. Could you try asking it in a simpler way — for example, mention a store name, a date, or a product type clearly?"
                st.markdown(friendly_msg)
                with st.expander("Technical details (for support team)"):
                    st.code(str(e))
                st.session_state.messages.append({"role": "assistant", "content": friendly_msg})