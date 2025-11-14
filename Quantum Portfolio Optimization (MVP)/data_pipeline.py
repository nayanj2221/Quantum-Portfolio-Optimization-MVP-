"""
Data Pipeline Module (data_pipeline.py)
This is our "Recipe Book". These are the main functions.

"""

# Step 1: Import necessary tools (libraries)
import yfinance as yf
import pandas as pd
import numpy as np
from typing import List, Tuple

# --- Recipe 1: Doing Data Fetch ---
def fetch_stock_data(tickers: List[str], start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch stock data from Yahoo Finance.
    """
    print(f"[Data Pipeline]: Fetching data for {tickers}...")
    try:
        # auto_adjust=True makes it easier to use Close prices.
        data = yf.download(tickers, start=start_date, end=end_date, progress=False, auto_adjust=True)
        
        # If data is empty then return an empty DataFrame
        if data.empty:
            print("[Data Pipeline]: Error: No data fetched. Check tickers or date range.")
            return pd.DataFrame()

        if len(tickers) == 1:
           # For a single stock, use the 'Close' column
            prices_df = data[['Close']].copy()
            prices_df.columns = tickers
        else:
            # When auto_adjust=True, yf.download provides adjusted prices in the 'Close' column
            prices_df = data['Close'].copy()
            
        prices_df = prices_df.dropna()
        print("[Data Pipeline]: Data fetching complete.")
        return prices_df
        
    except Exception as e:
        print(f"[Data Pipeline]: Error fetching data: {e}")
        return pd.DataFrame() 

# --- Recipe 2: Calculate Mu and Sigma (Subtask 2.2) ---
def calculate_mu_and_sigma(prices_df: pd.DataFrame) -> Tuple[pd.Series, pd.DataFrame]:
    """
    Calculate annualized expected returns (mu) and covariance matrix (Sigma).
    (This is Subtask 2.2)
    """
    print(f"[Data Pipeline]: Calculating mu and sigma...")
    
    # Calculate log returns
    log_returns = np.log(prices_df / prices_df.shift(1))
    
    # Drop the first row (which will be NaN)
    log_returns = log_returns.dropna()
    
    # Mu (Annualized Mean Return)
    mu = log_returns.mean() * 252
    
    # Sigma (Annualized Covariance Matrix)
    sigma = log_returns.cov() * 252
    
    print("[Data Pipeline]: Calculation complete.")
    return mu, sigma

# --- "Testing Block" ---
# This code only runs when you execute this file directly.
# If another file (for example main_project.py) imports this module,
# the block below will NOT run.
if __name__ == "__main__":
    
    print("\n---------------------------------------------------")
    print(">>> 'data_pipeline.py' was RUN DIRECTLY (Testing Mode)  <<<")
    print(">>> THIS IS NOT THE MAIN PROGRAM! THIS IS FOR TESTING ONLY. <<<")
    print("---------------------------------------------------")

    print("\n--- [Test Run] Starting (MVP Stocks) ---")
    
    # Test ke liye 4 stocks aur 3 saal ka data
    tickers_mvp = ['AAPL', 'GOOG', 'MSFT', 'AMZN'] 
    start_date = '2021-01-01'
    end_date = '2023-12-31'

    # Test 1: Call fetch function
    prices = fetch_stock_data(tickers=tickers_mvp, start_date=start_date, end_date=end_date)
    
    if not prices.empty:
        # Test 2: Call calculation function
        mu, sigma = calculate_mu_and_sigma(prices)
        
        print("\n--- [Test Run] Results ---")
        print("\nAnnualized Mu (μ):\n", mu)
        print("\nAnnualized Sigma (Σ):\n", sigma)
    else:
        print("Test Run Failed: Data nahi mila.")
# ...existing code...