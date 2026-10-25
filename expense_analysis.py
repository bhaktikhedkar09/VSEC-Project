"""
Personal Expense Analysis
Mini Project: Data Analysis & Visualization using Pandas, NumPy, Matplotlib and Seaborn.

Run:
    pip install -r requirements.txt
    python expense_analysis.py

Input:
    personal_expenses.csv (kept in the same folder as this script)

Output:
    outputs/cleaned_expenses.csv
    outputs/*.png charts
    outputs/analysis_summary.txt
"""
from pathlib import Path
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "personal_expenses.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="Set2")
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["axes.titlesize"] = 14
plt.rcParams["axes.labelsize"] = 11


def load_and_clean_data(path: Path) -> tuple[pd.DataFrame, dict]:
    """Load raw transactions and clean missing, duplicate and inconsistent data."""
    raw = pd.read_csv(path)
    original_rows = len(raw)
    df = raw.copy()

    # Standardize column names and text fields.
    df.columns = [c.strip() for c in df.columns]
    for col in ["Category", "Description", "Payment_Method", "Needs"]:
        df[col] = df[col].astype("string").str.strip()

    # Normalize common inconsistent labels.
    df["Category"] = df["Category"].str.title()
    df["Payment_Method"] = df["Payment_Method"].str.title()
    df["Needs"] = df["Needs"].str.title()

    # Parse dates and numeric amounts safely.
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Amount_INR"] = pd.to_numeric(df["Amount_INR"], errors="coerce")

    # Remove duplicate transactions using all transaction fields.
    before_dedup = len(df)
    df = df.drop_duplicates()
    duplicate_rows_removed = before_dedup - len(df)

    # Handle missing values. Unknown labels are explicit; missing amounts are
    # filled with the median amount so records remain usable for analysis.
    df["Description"] = df["Description"].fillna("Unknown description")
    df["Payment_Method"] = df["Payment_Method"].fillna("Unknown")
    df["Category"] = df["Category"].fillna("Other")
    df["Needs"] = df["Needs"].fillna("Unknown")

    valid_amounts = df["Amount_INR"].dropna()
    if valid_amounts.empty:
        raise ValueError("No valid numeric Amount_INR values found in the dataset.")
    median_amount = float(valid_amounts.median())
    missing_amounts_filled = int(df["Amount_INR"].isna().sum())
    df["Amount_INR"] = df["Amount_INR"].fillna(median_amount)

    # Drop rows with invalid dates and invalid/non-positive amounts.
    invalid_date_rows = int(df["Date"].isna().sum())
    df = df.dropna(subset=["Date"])
    invalid_amount_rows = int((df["Amount_INR"] <= 0).sum())
    df = df[df["Amount_INR"] > 0].copy()

    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    df["Year"] = df["Date"].dt.year
    df["Day_Name"] = df["Date"].dt.day_name()
    df = df.sort_values("Date").reset_index(drop=True)

    cleaning_log = {
        "original_rows": original_rows,
        "duplicate_rows_removed": duplicate_rows_removed,
        "missing_amounts_filled_with_median": missing_amounts_filled,
        "invalid_date_rows_removed": invalid_date_rows,
        "non_positive_amount_rows_removed": invalid_amount_rows,
        "final_rows": len(df),
        "median_used_for_missing_amount": round(median_amount, 2),
    }
    return df, cleaning_log


def perform_analysis(df: pd.DataFrame) -> dict:
    """Use Pandas and NumPy to calculate summary statistics and comparisons."""
    amounts = df["Amount_INR"].to_numpy(dtype=float)  # NumPy array
    total_spending = float(np.sum(amounts))
    average_transaction = float(np.mean(amounts))
    median_transaction = float(np.median(amounts))
    standard_deviation = float(np.std(amounts, ddof=0))
    min_transaction = float(np.min(amounts))
    max_transaction = float(np.max(amounts))

    category_summary = (
        df.groupby("Category", as_index=False)
        .agg(Total_Spending=("Amount_INR", "sum"),
             Transactions=("Transaction_ID", "count"),
             Average_Transaction=("Amount_INR", "mean"))
        .sort_values("Total_Spending", ascending=False)
    )
    monthly_summary = (
        df.groupby("Month", as_index=False)
        .agg(Total_Spending=("Amount_INR", "sum"),
             Transactions=("Transaction_ID", "count"))
        .sort_values("Month")
    )
    payment_summary = (
        df.groupby("Payment_Method", as_index=False)
        .agg(Total_Spending=("Amount_INR", "sum"),
             Transactions=("Transaction_ID", "count"))
        .sort_values("Total_Spending", ascending=False)
    )
    needs_summary = (
        df.groupby("Needs", as_index=False)
        .agg(Total_Spending=("Amount_INR", "sum"),
             Transactions=("Transaction_ID", "count"))
        .sort_values("Total_Spending", ascending=False)
    )

    category_summary["Share_Percent"] = (
        category_summary["Total_Spending"] / total_spending * 100
    )
    monthly_summary["Month_Label"] = pd.to_datetime(monthly_summary["Month"]).dt.strftime("%b %Y")

    analysis = {
        "total_spending": total_spending,
        "transaction_count": int(len(df)),
        "average_transaction": average_transaction,
        "median_transaction": median_transaction,
        "standard_deviation": standard_deviation,
        "min_transaction": min_transaction,
        "max_transaction": max_transaction,
        "highest_category": str(category_summary.iloc[0]["Category"]),
        "highest_category_amount": float(category_summary.iloc[0]["Total_Spending"]),
        "highest_month": str(monthly_summary.loc[monthly_summary["Total_Spending"].idxmax(), "Month"]),
        "highest_month_amount": float(monthly_summary["Total_Spending"].max()),
        "category_summary": category_summary,
        "monthly_summary": monthly_summary,
        "payment_summary": payment_summary,
        "needs_summary": needs_summary,
    }
    return analysis


def make_visualizations(df: pd.DataFrame, analysis: dict) -> None:
    """Create charts and save each chart as a PNG file."""
    category = analysis["category_summary"]
    monthly = analysis["monthly_summary"]
    payment = analysis["payment_summary"]
    needs = analysis["needs_summary"]

    # 1. Spending by category.
    fig, ax = plt.subplots()
    sns.barplot(data=category, x="Total_Spending", y="Category", color="steelblue", ax=ax)
    ax.set_title("Total Spending by Category")
    ax.set_xlabel("Spending (INR)")
    ax.set_ylabel("Category")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "01_spending_by_category.png", dpi=160)
    plt.close(fig)

    # 2. Monthly spending trend.
    fig, ax = plt.subplots()
    sns.lineplot(data=monthly, x="Month_Label", y="Total_Spending", marker="o", ax=ax)
    ax.set_title("Monthly Spending Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Spending (INR)")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "02_monthly_spending_trend.png", dpi=160)
    plt.close(fig)

    # 3. Spending share by category.
    fig, ax = plt.subplots()
    ax.pie(category["Total_Spending"], labels=category["Category"],
           autopct="%1.1f%%", startangle=90, pctdistance=0.78)
    ax.set_title("Share of Total Spending by Category")
    ax.axis("equal")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "03_category_spending_share.png", dpi=160)
    plt.close(fig)

    # 4. Payment method comparison.
    fig, ax = plt.subplots()
    sns.barplot(data=payment, x="Payment_Method", y="Total_Spending", color="steelblue", ax=ax)
    ax.set_title("Spending by Payment Method")
    ax.set_xlabel("Payment Method")
    ax.set_ylabel("Spending (INR)")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "04_payment_method_comparison.png", dpi=160)
    plt.close(fig)

    # 5. Amount distribution.
    fig, ax = plt.subplots()
    sns.histplot(data=df, x="Amount_INR", bins=20, kde=True, color="steelblue", ax=ax)
    ax.set_title("Distribution of Transaction Amounts")
    ax.set_xlabel("Transaction amount (INR)")
    ax.set_ylabel("Number of transactions")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "05_transaction_amount_distribution.png", dpi=160)
    plt.close(fig)

    # 6. Needs versus wants.
    fig, ax = plt.subplots()
    sns.barplot(data=needs, x="Needs", y="Total_Spending", color="steelblue", ax=ax)
    ax.set_title("Spending on Needs versus Wants")
    ax.set_xlabel("Expense type")
    ax.set_ylabel("Spending (INR)")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "06_needs_vs_wants.png", dpi=160)
    plt.close(fig)


def write_summary(df: pd.DataFrame, analysis: dict, cleaning: dict) -> None:
    """Save tables and a human-readable summary report."""
    analysis["category_summary"].to_csv(OUTPUT_DIR / "category_summary.csv", index=False)
    analysis["monthly_summary"].to_csv(OUTPUT_DIR / "monthly_summary.csv", index=False)
    analysis["payment_summary"].to_csv(OUTPUT_DIR / "payment_method_summary.csv", index=False)
    analysis["needs_summary"].to_csv(OUTPUT_DIR / "needs_wants_summary.csv", index=False)
    df.to_csv(OUTPUT_DIR / "cleaned_expenses.csv", index=False)

    money = lambda x: f"₹{x:,.2f}"
    lines = [
        "PERSONAL EXPENSE ANALYSIS — AUTOMATED SUMMARY",
        "=" * 48,
        f"Transactions analyzed: {analysis['transaction_count']}",
        f"Total spending: {money(analysis['total_spending'])}",
        f"Average transaction: {money(analysis['average_transaction'])}",
        f"Median transaction: {money(analysis['median_transaction'])}",
        f"Standard deviation: {money(analysis['standard_deviation'])}",
        f"Smallest transaction: {money(analysis['min_transaction'])}",
        f"Largest transaction: {money(analysis['max_transaction'])}",
        "",
        "KEY FINDINGS",
        f"- Highest-spending category: {analysis['highest_category']} "
        f"({money(analysis['highest_category_amount'])}).",
        f"- Highest-spending month: {analysis['highest_month']} "
        f"({money(analysis['highest_month_amount'])}).",
        f"- Category spending share: see category_summary.csv.",
        f"- Payment method comparison: see payment_method_summary.csv.",
        "",
        "DATA CLEANING LOG",
    ]
    lines.extend([f"- {key.replace('_', ' ').capitalize()}: {value}" for key, value in cleaning.items()])
    lines.extend([
        "",
        "Note: This is a synthetic sample dataset created for an academic mini-project.",
        "Findings demonstrate the method and should not be treated as anyone's real finances.",
    ])
    (OUTPUT_DIR / "analysis_summary.txt").write_text("\n".join(lines), encoding="utf-8")


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}\nKeep personal_expenses.csv beside this script."
        )
    df, cleaning_log = load_and_clean_data(DATA_FILE)
    results = perform_analysis(df)
    make_visualizations(df, results)
    write_summary(df, results, cleaning_log)

    print("\nPERSONAL EXPENSE ANALYSIS COMPLETE")
    print("-" * 38)
    print(f"Transactions analyzed : {results['transaction_count']}")
    print(f"Total spending        : ₹{results['total_spending']:,.2f}")
    print(f"Average transaction  : ₹{results['average_transaction']:,.2f}")
    print(f"Highest category      : {results['highest_category']}")
    print(f"Highest-spending month: {results['highest_month']}")
    print(f"\nOutputs saved in: {OUTPUT_DIR}")
    print("Open outputs/analysis_summary.txt for the summary and outputs/*.png for charts.")


if __name__ == "__main__":
    main()
