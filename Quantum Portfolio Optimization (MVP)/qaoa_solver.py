"""
QAOA Solver (qaoa_solver.py)
Its job is to take the Ising Hamiltonian 
and solve it using the QAOA algorithm to produce the final result.
"""

# Step 1: Import necessary tools

from qiskit_algorithms.minimum_eigensolvers import QAOA
from qiskit_algorithms.optimizers import COBYLA

# We use the default sampler from qiskit.primitives.
from qiskit.primitives import StatevectorSampler as Sampler

# For representing Pauli operators (Z)
from qiskit.quantum_info import SparsePauliOp
# Type hints
from typing import List, Tuple, Dict
import numpy as np
# QuadraticProgram type (imported elsewhere)
from qiskit_optimization import QuadraticProgram
import json

# --- Function to Solve with QAOA ---

def solve_with_qaoa(hamiltonian: SparsePauliOp) -> Dict:
    """
    Take an Ising Hamiltonian and solve it using QAOA.
    """
    print("[QAOA Solver]: Setting up the QAOA engine...")
    
     # 1. Classical optimizer
    optimizer = COBYLA()
    
    # 2. Quantum sampler (simulator)
    simulator = Sampler()

    # 3. Build QAOA instance
    reps = 1 # number of QAOA layers (p=1)
    qaoa_engine = QAOA(sampler=simulator, optimizer=optimizer, reps=reps)
    
    print("[QAOA Solver]: Solving the Hamiltonian (searching for best solution)...")
    
    # 4. Engine ko chalaana
    result = qaoa_engine.compute_minimum_eigenvalue(hamiltonian)
    
    print("[QAOA Solver]: Solution obtained.")
    
    # 5. Return the raw result
    return result

def interpret_result(result: Dict, tickers: List[str], qp: 'QuadraticProgram') -> Tuple[List[str], float]:
    """
    Convert the raw QAOA result into human-friendly output (stock names).
    """
    
    # ***** FIX APPLIED HERE *****
    # In recent Qiskit versions, result.eigenstate is a dictionary mapping bitstrings to counts.
    
    eigenstate_dict = result.eigenstate
    print(f"[Interpreter]: Raw eigenstate dictionary (solution_str: counts): {eigenstate_dict}")

    # Select the bitstring with the highest count
    best_solution_str = max(eigenstate_dict, key=eigenstate_dict.get)

    # Use that string directly as the binary solution
    binary_string = best_solution_str
  
    
    print(f"[Interpreter]: Best binary string result: {binary_string}")
    
    selected_stocks = []
    # Qiskit bitstrings may be little-endian (e.g., 'x_3 x_2 x_1 x_0'), so reverse to match tickers

    reversed_binary_string = binary_string[::-1]
    
    for i in range(len(tickers)):
        if reversed_binary_string[i] == '1':
            selected_stocks.append(tickers[i])
            
    # Compute the actual objective value using the original QuadraticProgram
    solution_vector = [int(bit) for bit in reversed_binary_string]

    final_score = qp.objective.evaluate(solution_vector)
            
    return selected_stocks, final_score


# --- "Testing Block" ---
# This code runs only when this file is executed directly.
if __name__ == "__main__":
    
    print("\n---------------------------------------------------------")
    print(">>> 'qaoa_solver.py' was RUN DIRECTLY (Testing Mode) <<<")
    print(">>> THIS WILL RUN THE ENTIRE PIPELINE  <<<")
    print("---------------------------------------------------------")
    
    # --- Imports (depending on your file structure) ---
    try:
        from data_pipeline import fetch_stock_data, calculate_mu_and_sigma
        print("Note: 'data_pipeline.py' ko import kiya.")
    except ImportError:
        print("FATAL ERROR: 'data_pipeline.py' file not found. Cannot run test.")
        exit()
        
    try:
        from problem_builder import create_quadratic_program
        print("Note: Imported 'data_pipeline.py'.")
    except ImportError:
        print("FATAL ERROR: 'data_pipeline.py' file not found. Cannot run test.")
        exit()
        
    try:
        from hamiltonian_converter import convert_to_ising
        print("Note: Imported 'problem_builder.py'.")
    except ImportError:
        print("FATAL ERROR: 'hamiltonian_converter.py' file not found. Cannot run test.")
        exit()

    # --- Step 1: Fetch Data  ---
    print("\n--- [Test Run] Step 1: Data Laana ---")
    tickers_mvp = ['AAPL', 'GOOG', 'MSFT', 'AMZN'] # n=4
    start_date = '2021-01-01'
    end_date = '2024-12-31'
    
    prices = fetch_stock_data(tickers=tickers_mvp, start_date=start_date, end_date=end_date)
    
    if prices is not None and not prices.empty:
        mu, sigma = calculate_mu_and_sigma(prices)
        
        # --- Step 2: Build Problem  ---
        print("\n--- [Test Run] Step 2: Qiskit Problem Banana (Objective + Constraint) ---")
        k_budget = 2 # k=2  select 2 assets
        q_risk = 1.0 # q=1 risk weight
        
        qp_problem = create_quadratic_program(mu, sigma, k=k_budget, q=q_risk)
        
        # --- Step 3: Hamiltonian Convert Karna  ---
        print("\n--- [Test Run] Step 3: Convert to Ising Hamiltonian (QUBO -> Ising) ---")
        
        hamiltonian, offset = convert_to_ising(qp_problem)
        
        if hamiltonian is not None:
             # --- Step 4: Solve Problem  ---
            print("\n--- [Test Run] Step 4: Solve with QAOA ---")
            
            raw_result = solve_with_qaoa(hamiltonian)
            
            print("\n--- [Test Run] Step 5: Display Final Result ---")
            stocks, score = interpret_result(raw_result, tickers_mvp, qp_problem)
            
            # Convert result to human-readable form            
            print("\n=================================================")
            print("          FINAL OPTIMAL PORTFOLIO RESULT          ")
            print("=================================================")
            print(f"Optimal Score (Risk-Return): {score:.4f}")
            print(f"Chune gaye Stocks (k=2): {stocks}")
            print("=================================================")
            # ***** NEW STEP: Save results to JSON *****
            print(f"\n--- [Test Run] Step 6: Saving result to 'results.json' ---")
            

            result_data = {
                "selected_stocks": stocks,
                "optimal_score": score,
                "parameters": {
                    "tickers": tickers_mvp,
                    "k_budget": k_budget,
                    "q_risk": q_risk
                },
                
                # Use the raw_result.eigenstate dictionary
                "raw_eigenstate_dict": raw_result.eigenstate
            }
            
            try:
               
                with open("results.json", "w") as f:
                    # 'json.dump' ka istemal karke dictionary ko file mein likh denge
                    # indent=4 se file sundar dikhti hai (pretty-print)
                    json.dump(result_data, f, indent=4, default=str) # default=str sureksha ke liye
                print("Result successfully saved to 'results.json'.")
            except Exception as e:
                print(f"Error: Result not save :  {e}")
            # ***** BADLAV KHATM *****

        else:
            print("Test Run Failed: Hamiltonian not  conversion .")
    else:
        print("Test Run Failed: Data not found .")