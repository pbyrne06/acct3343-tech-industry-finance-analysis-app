import math

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Tech & Software Screener",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Safely load and process CSS styles using single-quote formatting to avoid nested parser issues
css_style = '''<style>
[data-testid="stAppViewContainer"] {background-color: #0B0F19; color: #F3F4F6;}
[data-testid="stSidebar"] {background-color: #111827; border-right: 1px solid #1F2937;}
h1, h2, h3 {font-family: 'Inter', sans-serif; font-weight: 700; color: #F3F4F6; letter-spacing: -0.025em;}
div[data-testid="stMarkdownContainer"] h1 {color: #60A5FA; margin-bottom: 5px;}
div[data-testid="stMarkdownContainer"] h2 {color: #38BDF8; border-bottom: 2px solid #1F2937; padding-bottom: 8px;}
div[data-testid="metric-container"] {background-color: #1F2937; padding: 20px; border-radius: 12px; border: 1px solid #374151;}
.insight-box {background-color: #1F2937; padding: 20px 22px; border-radius: 12px; border-left: 5px solid #3B82F6; margin: 14px 0 25px 0;}
.insight-box h4 {margin-top: 0; color: #60A5FA; font-size: 1.1rem;}
.insight-box p {margin-bottom: 0; color: #D1D5DB; font-size: 0.95rem; line-height: 1.6;}
.app-footer {color: #9CA3AF; font-size: 0.82rem; text-align: center; margin-top: 10px;}
</style>'''

st.markdown(css_style, unsafe_allow_html=True)

# --- App Headers ---
st.title("📊 Tech & Software Screener")
st.caption("ACCT 3343 · Financial Accounting Analysis")
st.write("Screen 100 technology and software companies with quantitative filters for quality, value, and risk — and build a Buy or Sell list in seconds.")

@st.cache_data
def load_data():
    df = pd.read_csv('universe.csv')
    df = df.rename(columns={
        'Metric_1_STA': 'STA',
        'Metric_2_Z_Score': 'Altman Z-Score',
        'Metric_3_SNOA': 'SNOA',
        'Metric_4_GPA': 'Gross Profitability (GPA)',
        'Metric_5_BM': 'Book-to-Market (B/M)',
        'Metric_6_DE': 'Debt-to-Equity (D/E)',
        'Metric_7_PS': 'Price-to-Sales (P/S)'
    })
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("universe.csv was not found. Please make sure universe.csv is in the same folder as this app.")
    st.stop()

# --- Intro Panel ---
st.markdown('<div class="insight-box"><h4>How This Screener Works</h4><p>Technology and software companies grow by investing in intangible assets, so this screener uses benchmarks calibrated for the sector rather than one-size-fits-all cut-offs. The filters start at sensible defaults that surface companies with strong profit generation, solid balance sheets, and reasonable valuations — and flag firms showing warning signs such as high accruals or financial distress. Move any slider in the sidebar and both lists update instantly.</p></div>', unsafe_allow_html=True)

# --- Sidebar Controls ---
st.sidebar.header("Filter Adjustments")
st.sidebar.caption("Slider ranges are rounded to whole numbers. Defaults are pre-set for a balanced starting list.")

def whole_bounds(series):
    """Round a slider's range outward to whole numbers (floor the min, ceil the max)."""
    return float(math.floor(series.dropna().min())), float(math.ceil(series.dropna().max()))

# --- SELL SIDE FILTERS ---
st.sidebar.markdown("### 🔴 SELL Side (Risk Flags)")
sta_lo, sta_hi = whole_bounds(df['STA'])
sta_max = st.sidebar.slider("Max Accruals (STA)", min_value=sta_lo, max_value=sta_hi, value=0.15, help="Flags companies with excessive non-cash earnings.")
st.sidebar.caption("Filters out firms with suspicious non-cash adjustments.")

z_lo, z_hi = whole_bounds(df['Altman Z-Score'])
z_min = st.sidebar.slider("Min Altman Z-Score", min_value=z_lo, max_value=z_hi, value=1.5, help="Bankruptcy proxy.")
st.sidebar.caption("Flags companies under significant distress.")

snoa_lo, snoa_hi = whole_bounds(df['SNOA'])
snoa_max = st.sidebar.slider("Max SNOA", min_value=snoa_lo, max_value=snoa_hi, value=0.90, help="Balance sheet asset bloating.")

# --- BUY SIDE FILTERS ---
st.sidebar.markdown("### 🟢 BUY Side (Value & Quality)")
gpa_lo, gpa_hi = whole_bounds(df['Gross Profitability (GPA)'])
gpa_min = st.sidebar.slider("Min Gross Profitability (GPA)", min_value=gpa_lo, max_value=gpa_hi, value=0.20)
st.sidebar.caption("Ensures business actively generates profit.")

bm_lo, bm_hi = whole_bounds(df['Book-to-Market (B/M)'])
bm_min = st.sidebar.slider("Min Book-to-Market (B/M)", min_value=bm_lo, max_value=bm_hi, value=0.03)
st.sidebar.caption("Value factor adjustment for tech multiple levels.")

ps_lo, ps_hi = whole_bounds(df['Price-to-Sales (P/S)'])
max_ps = st.sidebar.slider("Max Price-to-Sales (P/S)", min_value=ps_lo, max_value=ps_hi, value=25.0)

de_lo, de_hi = whole_bounds(df['Debt-to-Equity (D/E)'])
max_de = st.sidebar.slider("Max Debt-to-Equity (D/E)", min_value=de_lo, max_value=de_hi, value=2.0)

# Filter logic
sell_candidates = df[(df['STA'] > sta_max) | (df['Altman Z-Score'] < z_min) | (df['SNOA'] > snoa_max)]
buy_candidates = df[(df['Gross Profitability (GPA)'] >= gpa_min) & (df['Book-to-Market (B/M)'] >= bm_min) & (df['Price-to-Sales (P/S)'] <= max_ps) & (df['Debt-to-Equity (D/E)'] <= max_de)]

col1, col2, col3 = st.columns(3)
col1.metric("Total Universe", f"{len(df)} Firms")
col2.metric("🔴 Sell Flags", f"{len(sell_candidates)} Firms")
col3.metric("🟢 Buy Candidates", f"{len(buy_candidates)} Firms")

st.markdown("--- ")
st.header("🔴 Sell Candidate Portfolio")
st.caption("Flagged when accruals, financial distress, or balance-sheet bloat pass a risk threshold above.")
if not sell_candidates.empty:
    display_sell = sell_candidates[['Ticker', 'Company_Name', 'STA', 'Altman Z-Score', 'SNOA']]
    st.dataframe(display_sell.style.background_gradient(cmap='Reds', subset=['STA', 'SNOA']).format({'STA': '{:.4f}', 'Altman Z-Score': '{:.2f}', 'SNOA': '{:.4f}'}), use_container_width=True)
else:
    st.success("No companies meet high-risk flags.")

st.markdown("--- ")
st.header("🟢 Buy Candidate Portfolio")
st.caption("Meets every quality and value threshold above: profitability, book-to-market, price-to-sales, and leverage.")
if not buy_candidates.empty:
    display_buy = buy_candidates[['Ticker', 'Company_Name', 'Gross Profitability (GPA)', 'Book-to-Market (B/M)', 'Debt-to-Equity (D/E)', 'Price-to-Sales (P/S)']]
    st.dataframe(display_buy.style.background_gradient(cmap='Greens', subset=['Gross Profitability (GPA)', 'Book-to-Market (B/M)']).format({'Gross Profitability (GPA)': '{:.4f}', 'Book-to-Market (B/M)': '{:.4f}', 'Debt-to-Equity (D/E)': '{:.2f}', 'Price-to-Sales (P/S)': '{:.2f}'}), use_container_width=True)
else:
    st.warning("No buy candidates found. Try loosening your sidebar sliders.")

st.markdown("--- ")
st.markdown('<p class="app-footer">Tech &amp; Software Screener · Universe of 100 companies · For informational and educational purposes only — not investment advice.</p>', unsafe_allow_html=True)
