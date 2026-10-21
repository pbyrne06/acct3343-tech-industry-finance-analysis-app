# Tech & Software Screener

An interactive stock-screening app for technology and software companies, built with Streamlit.

Screen a universe of **100 companies** using seven financial filters calibrated for the tech sector:

- **Sell side (risk flags):** Max Accruals (STA), Min Altman Z-Score, Max SNOA
- **Buy side (value & quality):** Min Gross Profitability (GPA), Min Book-to-Market (B/M), Max Price-to-Sales (P/S), Max Debt-to-Equity (D/E)

Adjust the sliders in the sidebar and the Sell Flag and Buy Candidate portfolios update instantly.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Files

- `app.py` — the Streamlit app
- `universe.csv` — the 100-company universe and its financial metrics
- `requirements.txt` — Python dependencies
- `.streamlit/config.toml` — app theme

*Built for ACCT 3343 — Financial Accounting Analysis. For informational and educational purposes only — not investment advice.*
