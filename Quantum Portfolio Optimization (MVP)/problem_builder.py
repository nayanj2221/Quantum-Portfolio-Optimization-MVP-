"""
Qiskit Problem Builder (problem_builder.py)

Its job is to take mu (μ) and sigma (Σ) from the data_pipeline
and convert them into a Qiskit QuadraticProgram object.
"""

# Step 1: Import necessary tools 
import pandas as pd

# Import the main Qiskit optimization class
from qiskit_optimization import QuadraticProgram
# Typing (optional, but good practice)
from typing import Tuple

# --- Function to build the Qiskit Problem ---

def create_quadratic_program(mu: pd.Series, sigma: pd.DataFrame, k: int, q: float = 1.0) -> QuadraticProgram:
    """
     Create a Qiskit QuadraticProgram object using mu, sigma, k, and q.
    """
    print(f"[Problem Builder]: Creating Quadratic Program for n={len(mu)} assets, k={k}, q={q}...")
    
    # n = number of assets (e.g., 4)
    n = len(mu)
    
    # --- Step 3.2.1: Start QuadraticProgram ---
    # Create an empty QuadraticProgram.
    qp = QuadraticProgram(name="PortfolioOptimization")
    
       # Define 'n' binary decision variables named 'x'
    
    qp.binary_var_list(n, name="x")

    # --- Step 3.2.2: Set Objective ---
    # Our objective: Minimize q*(Risk) - (Return)
    #
    # Return (linear part): -mu
    # (Negative because we want to maximize return, which is equivalent to minimizing -return)
    linear_objective = -mu.values
    
    # Risk (Quadratic part): q * sigma
    quadratic_objective = q * sigma.values
    
    # Tell Qiskit to minimize this objective
    qp.minimize(linear=linear_objective, quadratic=quadratic_objective)
    
    # --- Step : Set Constraint ---
    # Constraint: x_0 + x_1 + x_2 + x_3 = k (e.g., k=2)
    #
    # ***** CHANGE MADE HERE (THE FIX) *****
    # We replaced {'x': [1]*n} (dictionary) with [1]*n (list).
    # This tells Qiskit to multiply all variables by 1.

    qp.linear_constraint(linear=[1]*n, sense='==', rhs=k, name="budget_constraint")
    
    print("[Problem Builder]: Quadratic Program created.")
    
    # Return the final QuadraticProgram
    return qp

# --- "Testing Block" ---
# This code only runs when you execute this file directly.
if __name__ == "__main__":
    
    print("\n---------------------------------------------------")
    print(">>> 'problem_builder.py' was RUN DIRECTLY (Testing Mode) <<<")
    print("---------------------------------------------------")
    
    # For testing we need (data_pipeline) data
    try:
        # ** YEH LINE AAPKE FILE STRUCTURE KE LIYE HAI: **
        from data_pipeline import fetch_stock_data, calculate_mu_and_sigma
        print("Note: 'data_pipeline.py' ko same folder se import kar raha hoon.")
        
    except ImportError:
        print("FATAL ERROR: 'data_pipeline.py' file not found. Cannot run test.")
        print("Ensure 'data_pipeline.py' is in the same folder as 'problem_builder.py'.")
        exit()


       # --- Step 1: Fetch Data  ---
    print("\n--- [Test Run] Step 1: Data Laana ---")
    tickers_mvp = ['AAPL', 'GOOG', 'MSFT', 'AMZN'] # 4 stocks (n=4)
    start_date = '2021-01-01'
    end_date = '2023-12-31'
    
    prices = fetch_stock_data(tickers=tickers_mvp, start_date=start_date, end_date=end_date)
    
    if prices is not None and not prices.empty:
        mu, sigma = calculate_mu_and_sigma(prices)
        
        # --- Step 2: Build Problem  ---
        print("\n--- [Test Run] Step 2: Build Qiskit Problem ---")
        k_budget = 2 # choose 2 out of 4 stocks
        q_risk = 1.0 # risk weight (default)
        
        # Call our function
        qp_problem = create_quadratic_program(mu, sigma, k=k_budget, q=q_risk)
        
        # --- Step 3: Show Result ---
        print("\n--- [Test Run] Result: Qiskit Quadratic Program (Pretty Print) ---")
        # .prettyprint() displays the problem in a readable format
        print(qp_problem.prettyprint())
        
    else:
        print("Test Run Failed: No data retrieved.")
# ...existing code...