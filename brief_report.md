# Mini Project Report: Personal Expense Analysis

## 1. Title
**Personal Expense Analysis using Python**

## 2. Aim
To analyze personal expense records by cleaning a CSV dataset with Pandas, applying numerical analysis with NumPy, and presenting useful spending patterns through Matplotlib and Seaborn visualizations.

## 3. Problem Statement
People often make small daily purchases without tracking where their money goes. This project organizes transaction records and summarizes spending by category, month, payment method, and expense type (need or want). The results can help a person understand spending patterns and make a more informed budget.

## 4. Tools and Technologies
- **Python:** programming language.
- **Pandas:** CSV handling, data cleaning, grouping, and summary tables.
- **NumPy:** numerical calculations such as total, mean, median, standard deviation, minimum, and maximum.
- **Matplotlib and Seaborn:** visualizations.
- **CSV:** simple dataset format.

## 5. Dataset Description
The sample dataset contains transaction ID, date, category, description, amount in Indian rupees, payment method, and whether the expense is a need or a want. It contains synthetic transactions across a calendar year. A few intentional data issues (missing values, inconsistent capitalization, and a duplicate record) are included to demonstrate cleaning. The dataset is not based on real personal finances.

## 6. Methodology
1. Read the CSV file using Pandas.
2. Standardize text values and category capitalization.
3. Convert dates and amounts to suitable data types.
4. Remove duplicate transactions.
5. Fill missing descriptions and labels with explicit placeholders.
6. Fill a missing amount using the median of valid amounts, and remove invalid dates or non-positive amounts.
7. Use NumPy to calculate summary statistics.
8. Use Pandas group-by operations to summarize spending by category, month, payment method, and needs/wants.
9. Generate charts and save the cleaned dataset, summary tables, and key findings.

## 7. Visualizations
The program generates these charts:
1. **Total Spending by Category:** compares the total amount spent in each category.
2. **Monthly Spending Trend:** shows how total spending changes over the year.
3. **Share of Total Spending by Category:** shows each category's proportion of total spending.
4. **Spending by Payment Method:** compares spending across payment types.
5. **Distribution of Transaction Amounts:** shows common transaction sizes and the spread of amounts.
6. **Needs versus Wants:** compares spending on essential and discretionary items.

## 8. Results and Discussion
Run `expense_analysis.py` to generate results for the included dataset. The console and `outputs/analysis_summary.txt` show total spending, transaction count, average and median transaction, standard deviation, highest-spending category, and highest-spending month. The CSV summary files provide detailed breakdowns. Since the sample data is synthetic, results are illustrative only and will not describe an actual person's expenses.

## 9. Limitations
- The dataset is synthetic and relatively small.
- Filling a missing amount with the median preserves a row but may not reflect its true value.
- The project summarizes past records; it does not forecast future spending.
- Categories and the needs/wants labels depend on the quality of the recorded data.

## 10. Future Scope
The project can be improved with a graphical dashboard, budget limits and overspending alerts, import of bank statement CSV files, monthly budget comparisons, and interactive charts.

## 11. Conclusion
The project demonstrates a complete basic data-analysis workflow in Python. Pandas is used to clean and organize transactions, NumPy calculates numerical summaries, and Matplotlib/Seaborn communicate spending patterns through charts. The generated summaries can support better awareness of expenses and more informed budgeting.

## 12. How to Execute
Install the packages with `python -m pip install -r requirements.txt`, then run `python expense_analysis.py`. The generated charts, cleaned data, and summary reports are saved in the `outputs` folder.
