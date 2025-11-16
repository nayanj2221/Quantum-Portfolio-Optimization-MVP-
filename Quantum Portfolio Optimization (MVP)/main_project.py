"""
Main Project File (main_project.py)
This is our main program which will use 'data_pipeline'.

This file imports 'data_pipeline.py' and calls its functions
(such as fetch_stock_data).
"""

print(">>> 'main_project.py' is starting...")
print("    Now importing 'data_pipeline'...")

# --- Importing the module ---
# We import the 'data_pipeline.py' file.
# Python will read that file, but its if __name__ == "__main__" block WILL NOT run.


# If 'data_pipeline.py' is inside a 'src' folder:
try:
    from src import data_pipeline
    print("    Imported from 'src/data_pipeline.py'.")
# If 'data_pipeline.py' is in the same folder:
except ImportError:
    try:
        import data_pipeline
        print("    Imported from 'data_pipeline.py' (same folder).")
    except ImportError:
        print("\nFATAL ERROR: 'data_pipeline.py' not found.")
        print("Please ensure 'data_pipeline.py' is in the same folder or in a 'src' folder.")
        exit()  # Exit the program

print("\n>>> 'main_project.py': Import complete.")
print("    Now using functions from 'data_pipeline'.")

# --- Main work ---
# Fetch data for two different stocks and date range
my_tickers = ['AAPL', 'GOOG', 'MSFT', 'AMZN']  # Selected stocks
my_start = '2021-01-01'
my_end = '2023-12-31'

# 1. Use Recipe 1 (fetch_stock_data)
prices = data_pipeline.fetch_stock_data(tickers=my_tickers, start_date=my_start, end_date=my_end)

if not prices.empty:
    # 2. Use Recipe 2 (calculate_mu_and_sigma )
    mu, sigma = data_pipeline.calculate_mu_and_sigma(prices)
    
    print("\n---------------------------------------------------")
    print(">>> 'main_project.py' FINAL OUTPUT <<<")
    print("---------------------------------------------------")
    print("Project Mu (μ) [NVDA, TSLA]:\n", mu)
    print("\nProject Sigma (Σ) [NVDA, TSLA]:\n", sigma)
else:
    print("Project Failed: No data retrieved.")

print("\n>>> 'main_project.py' finished.")

# ...existing code...
