💸 Personal Expense Analysis
A Python mini project that analyzes personal expense records and presents the results through an interactive Streamlit dashboard. It demonstrates data cleaning, statistical analysis, and data visualization using Pandas, NumPy, Matplotlib, Seaborn, and Plotly.
✨ Features
- Interactive dashboard with summary cards:
  - Total spending
  - Number of transactions
  - Average transaction amount
  - Median transaction amount
- Filters for date range, category, payment method, and spending type
- Category-wise spending bar chart
- Spending share pie chart
- Monthly spending trend
- Payment method comparison
- Needs-versus-wants analysis
- Transaction amount distribution
- Searchable transaction table
- Download filtered transactions as a CSV file
- Optional upload of another CSV dataset with the required columns
🧰 Technologies Used
- Python — application logic
- Pandas — data cleaning and analysis
- NumPy — numerical/statistical operations
- Matplotlib and Seaborn — visualizations in the analysis script
- Plotly — interactive dashboard charts
- Streamlit — web-based user interface
📁 Project Structure
personal_expense_analysis_project/
├── app.py                       # Streamlit frontend/dashboard
├── expense_analysis.py          # Main data analysis script
├── personal_expenses.csv        # Sample transaction dataset
├── requirements.txt             # Python dependencies
├── brief_report.md              # Project report
└── outputs/                     # Generated charts and analysis summaries
The outputs/ folder is generated or updated when expense_analysis.py runs.
⚙️ Installation and Setup
1. Install Python
Install Python 3.10 or newer and make sure Python is available in your terminal.
2. Open the project folder
Open this folder in VS Code, then select Terminal → New Terminal.
3. Install dependencies
python -m pip install -r requirements.txt
If you only want to install the dashboard dependencies:
python -m pip install streamlit plotly pandas
▶️ Run the Interactive Dashboard
From the project folder, run:
python -m streamlit run app.py
Streamlit will show a local URL, usually:
http://localhost:8501
Open that URL in your browser to use the dashboard.
📊 Run the Analysis Script
To generate the static charts, cleaned dataset, and summary files in outputs/, run:
python expense_analysis.py
🗂️ Dataset Format
The included dataset is synthetic and intended for academic demonstration. The dashboard expects these columns when loading a CSV:
- Date
- Category
- Amount_INR
- Payment_Method
- Needs
The Description column is optional and is displayed when present.
🔒 Data and Privacy Note
Use sample or non-sensitive data when demonstrating the project. The included records are synthetic and are not real personal financial records.
👨‍🎓 Project Purpose
This project demonstrates how Python data-analysis libraries can be used to clean transaction data, summarize spending, identify patterns, and communicate results through charts and an interactive dashboard.
Academic mini project — Personal Expense Analysis