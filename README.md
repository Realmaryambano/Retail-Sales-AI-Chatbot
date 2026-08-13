# 🛍️ Bonanza Satrangi — Retail Sales AI Chatbot

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![Gemini API](https://img.shields.io/badge/Gemini-API-8E75B2?logo=googlegemini&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)
![License](https://img.shields.io/badge/License-Proprietary-red)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

**🔗 Live Demo:** [your-live-demo-link-here](https://your-live-demo-link-here.streamlit.app)

An AI-powered Streamlit dashboard that lets non-technical store/retail staff ask plain-English questions about sales data (across multiple Bonanza Satrangi stores) and get instant answers — totals, top stores, best-selling categories, day-wise sales, and more — without writing a single line of SQL or Excel formula.

Under the hood, natural-language questions are converted into pandas code by an LLM (Gemini) and executed live against the sales data, with the results rendered back as tables, figures, or chat responses.

---

## 📸 Screenshot

![Dashboard Screenshot](https://via.placeholder.com/1200x700.png?text=Dashboard+Screenshot+Coming+Soon)

---

## ✨ Features

- **Plain-language querying** — ask things like *"Which store sold the most on 5 August?"* and get a direct answer.
- **One-click quick questions** — top 5 stores, best-selling categories, total sales, sales by day.
- **Executive KPI strip** — total sales (PKR), items sold, total bills, and number of stores at a glance.
- **Chat-style interface** — full conversation history persists during the session.
- **Automatic model fallback** — tries multiple Gemini models (`gemini-3.5-flash` → `gemini-1.5-flash`, etc.) so the app keeps working even if a specific model is unavailable on your API key.
- **Resilient error handling** — friendly messages for end users, with technical error details tucked into an expandable panel for support/debugging.
- **Data auto-detection** — automatically loads the sales Excel file placed in the project folder.
- **Store name normalization** — cleans inconsistent casing/spacing in store names before analysis.

---

## 🗂️ Project Structure

```
Retail-Sales-AI-Chatbot/
│
├── app.py       # Streamlit dashboard + AI chatbot (main app)
├── index.py     # Data preparation script — merges monthly sales files into one dataset
├── requirements.txt
└── README.md
```

---

## ⚙️ How It Works

### 1. `index.py` — Data Preparation

Raw sales exports are provided as separate monthly Excel files (e.g. one for July, one for August). `index.py`:

1. Reads the individual monthly Excel exports (e.g. `1st July 2026 till 31st July 2026.xlsx` and `1st August 2026 till 10th August 2026.xlsx`).
2. Combines them into a single dataset with `pandas.concat`.
3. Standardizes `Transact_Date` to `DD/MM/YYYY` format.
4. Writes the merged result to `sales_july_1_to_august_10_2026.xlsx`, which is the file `app.py` reads.

Run this **once** whenever new monthly data needs to be merged in, before launching the dashboard.

### 2. `app.py` — The Dashboard & AI Assistant

1. Loads the merged sales Excel file (auto-detected from the project folder).
2. Displays KPI cards (total sales, items sold, total bills, stores) and quick-question shortcuts.
3. The user connects the assistant by pasting a **Gemini API key** in the sidebar (kept only in the session — never stored on disk).
4. When a question is asked, `app.py` builds a prompt describing the dataset's columns and rules, sends it to Gemini, and receives back a small pandas snippet.
5. That snippet is executed against the in-memory DataFrame (`df`) and the resulting `result` variable — a number, a table, or text — is rendered in the chat.

### Data Columns

The sales dataset (as produced by `index.py`) contains:

| Column | Description |
|---|---|
| `Invoice_No` | Unique invoice/bill number |
| `Transact_Date` | Transaction date (DD/MM/YYYY) |
| `Store_Id` | Numeric store identifier |
| `Store_Name` | Store name (may have inconsistent casing/spacing — cleaned into `Store_Name_Clean`) |
| `Art_Grp_Id` | Product/article group ID |
| `Art_Grp_Descr` | Product category (e.g. Ladies Stitched Suits, Paper Bag) |
| `Design_Code` | Specific design/SKU code |
| `Quantity` | Units sold |
| `Unit_Price` | Price per unit |
| `Gross_Amount` | Amount before discount |
| `Total_Discount` | Discount applied |
| `Net_Sale` | Final revenue (PKR) — includes negative values for returns/refunds |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- A Google **Gemini API key** ([get one here](https://aistudio.google.com/app/apikey))

### 1. Clone the repository

```bash
git clone https://github.com/Realmaryambano/Retail-Sales-AI-Chatbot.git
cd Retail-Sales-AI-Chatbot
```

### 2. Install dependencies

```bash
pip install streamlit pandas openpyxl google-genai
```

Or, if a `requirements.txt` is provided:

```bash
pip install -r requirements.txt
```

### 3. Prepare the sales data

Place your monthly raw Excel exports in the project folder, update the filenames inside `index.py` if needed, then run:

```bash
python index.py
```

This generates `sales_july_1_to_august_10_2026.xlsx` in the project folder — the file the dashboard reads.

> You can skip this step if you already have a merged Excel file; just make sure it's a `.xlsx` file sitting in the project folder (the app will auto-detect the first one it finds if the expected filename isn't present).

### 4. Run the dashboard

```bash
streamlit run app.py
```

The app opens in your browser (usually `http://localhost:8501`).

### 5. Connect the assistant

In the sidebar, paste your Gemini API key and click **Turn On Assistant →**. Once connected, use a quick-question button or type your own question in the chat box at the bottom.

---

## 💬 Example Questions

- "Which 5 stores made the most total sales?"
- "Which 5 product categories sold the most pieces?"
- "What is the total sales amount, in PKR, across all stores?"
- "Show me the total sales for each day."
- "Which store sold the most on 5 August?"
- "How many Ladies Stitched Suits were sold in July?"

---

## 🔐 Notes on API Keys & Privacy

- The Gemini API key is entered per session and stored only in Streamlit's `session_state` — it is **not** written to disk or logged.
- Sales data stays local to wherever the app is running; only the natural-language question and column metadata are sent to the Gemini API to generate the analysis code — the underlying row-level data is not uploaded.

---

## 🧭 Roadmap / Ideas

- [ ] Add date-range filters and store filters in the sidebar
- [ ] Support charts/visualizations for trend questions
- [ ] Export chat answers as PDF/Excel reports
- [ ] Add authentication for multi-user/store-manager access
- [ ] Cache merged data automatically when new monthly files are added

---

## 👩‍💻 Author

**Maryam Bano**

- 📧 Email: [maryambano.official@gmail.com](mailto:maryambano.official@gmail.com)
- 💻 GitHub: [github.com/Realmaryambano](https://github.com/Realmaryambano/Retail-Sales-AI-Chatbot)
- 🔗 LinkedIn: [linkedin.com/in/realmaryambano](https://www.linkedin.com/in/realmaryambano/)

## 📜 License

This project is licensed under a proprietary license — all rights reserved. See [LICENSE](./LICENSE) for full details. Unauthorized copying, modification, or distribution of this software is prohibited without prior written consent from the author.
