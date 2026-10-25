from pathlib import Path
from io import BytesIO

import pandas as pd
import plotly.express as px
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATA = BASE_DIR / "personal_expenses.csv"

st.set_page_config(page_title="Personal Expense Analysis", page_icon="💸", layout="wide")
st.markdown("""
<style>
.main { background-color: #f7f9fc; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
[data-testid="stMetric"] { background: white; border: 1px solid #e5eaf2; padding: 16px 18px; border-radius: 14px; }
[data-testid="stMetricValue"] { color: #173b67; }
h1, h2, h3 { color: #173b67; }
</style>
""", unsafe_allow_html=True)

st.title("💸 Personal Expense Analysis")
st.caption("Explore spending patterns, categories, payment methods, and monthly trends.")

with st.sidebar:
    st.header("Dashboard controls")
    upload = st.file_uploader("Upload expense CSV (optional)", type=["csv"])
    st.caption("The included sample dataset is used if no file is uploaded.")

@st.cache_data
def load_data(uploaded_bytes=None):
    df = pd.read_csv(BytesIO(uploaded_bytes)) if uploaded_bytes else pd.read_csv(DEFAULT_DATA)
    required = {"Date", "Category", "Amount_INR", "Payment_Method", "Needs"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(sorted(missing)))
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Amount_INR"] = pd.to_numeric(df["Amount_INR"], errors="coerce")
    for col in ["Category", "Payment_Method", "Needs"]:
        df[col] = df[col].astype("string").str.strip().str.title()
    df = df.drop_duplicates().dropna(subset=["Date", "Amount_INR"])
    df = df[df["Amount_INR"] > 0].copy()
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df

try:
    data = load_data(upload.getvalue() if upload else None)
except Exception as exc:
    st.error(f"Could not load the dataset: {exc}")
    st.stop()
if data.empty:
    st.warning("No valid transactions found.")
    st.stop()

with st.sidebar:
    categories = sorted(data["Category"].dropna().unique().tolist())
    selected_categories = st.multiselect("Categories", categories, default=categories)
    methods = sorted(data["Payment_Method"].dropna().unique().tolist())
    selected_methods = st.multiselect("Payment methods", methods, default=methods)
    needs = sorted(data["Needs"].dropna().unique().tolist())
    selected_needs = st.multiselect("Spending type", needs, default=needs)
    min_date, max_date = data["Date"].min().date(), data["Date"].max().date()
    dates = st.date_input("Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

df = data[
    data["Category"].isin(selected_categories)
    & data["Payment_Method"].isin(selected_methods)
    & data["Needs"].isin(selected_needs)
].copy()
if isinstance(dates, (tuple, list)) and len(dates) == 2:
    start, end = pd.Timestamp(dates[0]), pd.Timestamp(dates[1]) + pd.Timedelta(days=1)
    df = df[(df["Date"] >= start) & (df["Date"] < end)]
if df.empty:
    st.warning("No transactions match the selected filters. Adjust the sidebar filters.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total spending", f"₹{df['Amount_INR'].sum():,.2f}")
c2.metric("Transactions", f"{len(df):,}")
c3.metric("Average transaction", f"₹{df['Amount_INR'].mean():,.2f}")
c4.metric("Median transaction", f"₹{df['Amount_INR'].median():,.2f}")

category = df.groupby("Category", as_index=False)["Amount_INR"].sum().sort_values("Amount_INR", ascending=False)
st.divider()
left, right = st.columns(2)
with left:
    st.subheader("Spending by category")
    fig = px.bar(category, x="Amount_INR", y="Category", orientation="h",
                 labels={"Amount_INR": "Spending (₹)", "Category": ""},
                 color="Amount_INR", color_continuous_scale="Blues")
    fig.update_layout(coloraxis_showscale=False, height=360, margin=dict(l=10, r=10, t=20, b=10))
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Share by category")
    fig = px.pie(category, names="Category", values="Amount_INR", hole=.45,
                 color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(height=360, margin=dict(l=10, r=10, t=20, b=10), legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Monthly spending trend")
    monthly = df.groupby("Month", as_index=False)["Amount_INR"].sum().sort_values("Month")
    monthly["Month_Label"] = pd.to_datetime(monthly["Month"]).dt.strftime("%b %Y")
    fig = px.line(monthly, x="Month_Label", y="Amount_INR", markers=True,
                  labels={"Month_Label": "Month", "Amount_INR": "Spending (₹)"})
    fig.update_traces(line=dict(width=3, color="#2878B5"), marker=dict(size=7))
    fig.update_layout(height=330, margin=dict(l=10, r=10, t=20, b=10))
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Payment method comparison")
    payment = df.groupby("Payment_Method", as_index=False)["Amount_INR"].sum()
    fig = px.bar(payment, x="Payment_Method", y="Amount_INR",
                 labels={"Payment_Method": "Payment method", "Amount_INR": "Spending (₹)"},
                 color="Payment_Method", color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(showlegend=False, height=330, margin=dict(l=10, r=10, t=20, b=10))
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Needs vs wants")
    needs_summary = df.groupby("Needs", as_index=False)["Amount_INR"].sum()
    fig = px.bar(needs_summary, x="Needs", y="Amount_INR",
                 labels={"Needs": "Spending type", "Amount_INR": "Spending (₹)"},
                 color="Needs", color_discrete_sequence=["#59A14F", "#E15759", "#9C9C9C"])
    fig.update_layout(showlegend=False, height=320, margin=dict(l=10, r=10, t=20, b=10))
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Transaction amount distribution")
    fig = px.histogram(df, x="Amount_INR", nbins=20,
                       labels={"Amount_INR": "Transaction amount (₹)"},
                       color_discrete_sequence=["#8F78B5"])
    fig.update_layout(height=320, margin=dict(l=10, r=10, t=20, b=10))
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("Transaction details")
search = st.text_input("Search descriptions, categories, or payment methods")
table = df.copy()
if search.strip():
    mask = table.astype(str).apply(lambda col: col.str.contains(search.strip(), case=False, na=False)).any(axis=1)
    table = table[mask]
cols = [c for c in ["Date", "Category", "Description", "Amount_INR", "Payment_Method", "Needs"] if c in table.columns]
display = table[cols].sort_values("Date", ascending=False).copy()
display["Date"] = display["Date"].dt.strftime("%d %b %Y")
display["Amount_INR"] = display["Amount_INR"].map(lambda x: f"₹{x:,.2f}")
st.dataframe(display, use_container_width=True, hide_index=True)
st.download_button("⬇️ Download filtered transactions as CSV", df.to_csv(index=False).encode("utf-8"),
                   file_name="filtered_expenses.csv", mime="text/csv")
st.caption("Academic demonstration only. The included sample data is synthetic.")
