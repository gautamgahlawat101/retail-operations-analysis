# retail-operations-analysis

This project is a retail analytics dashboard built with Python, Streamlit, pandas, and Plotly. It analyzes a large retail transaction dataset and presents business insights through interactive charts and KPI cards.

## Project Overview

The dashboard is designed to help users understand retail performance by exploring:

- revenue trends,
- city and store-type performance,
- customer segments,
- payment method distribution,
- best and worst-performing store-city combinations.

The project was built to support business decision-making through exploratory data analysis (EDA), KPI design, and interactive visualization.

## Project Structure

```text
Retail Data Analysis/
├── dashboard.py              # Main Streamlit dashboard app
├── Retail_Data_Analysis.ipynb  # Notebook with EDA and analysis steps
├── data/                     # CSV files used by the project
│   ├── df_cleaned.csv
│   ├── df_exploded_priced.csv
│   └── Retail_Transactions_Dataset_utf8.csv
├── models/                   # Optional folder for trained or saved models
├── requirements.txt          # Python dependencies
├── BUSINESS_PROBLEM_STATEMENT.md
├── FINAL_REPORT.md
├── .gitignore
└── README.md
```

## Data Files

The project uses the following data files:

- `df_cleaned.csv` - cleaned retail transaction dataset
- `df_exploded_priced.csv` - exploded dataset for product-level analysis
- `Retail_Transactions_Dataset_utf8.csv` - original/raw transaction dataset

## Technologies Used

- Python
- pandas
- Plotly
- Streamlit
- Jupyter Notebook

## How to Run Locally

1. Create a Python environment
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Run the dashboard
   ```bash
   streamlit run dashboard.py
   ```

## Notes

- The app uses local CSV files, so the data folder must stay intact when running the dashboard.
- For a smoother local run, you can use:
  ```bash
  streamlit run dashboard.py --server.headless true --server.fileWatcherType none --server.port 8501
  ```

## Business Value

This project demonstrates how a retail dataset can be transformed into an interactive business dashboard that supports monitoring, insight discovery, and decision-making.
