"""
Hamiltonian Converter (hamiltonian_converter.py)
Its job is to take a QuadraticProgram object (Task 3.2)
and convert it into an Ising Hamiltonian (input for QAOA).
"""

# Step 1: Import required tools
from qiskit_optimization import QuadraticProgram
# Pauli operators (Z) representation
from qiskit.quantum_info import SparsePauliOp
from typing import Tuple

# ***** FIX: Import converter to turn constrained problem into an unconstrained QUBO *****
from qiskit_optimization.converters import QuadraticProgramToQubo


# --- Function to Convert to Ising ---

def convert_to_ising(qp: QuadraticProgram) -> Tuple[SparsePauliOp, float]:
    """
    Take a QuadraticProgram object and convert it to
    an Ising Hamiltonian (SparsePauliOp) and an offset.
    """
    
    # Step A: First, convert constraints into QUBO penalties 
    # Use QuadraticProgramToQubo for that.
    print("[Converter]: Step A: Converting constraints into QUBO penalties...")
    qubo_converter = QuadraticProgramToQubo()
    qp_unconstrained = qubo_converter.convert(qp)
    
    # Now 'qp_unconstrained' is a new problem object with no constraints.
    
    # Step B: Convert this unconstrained QUBO to an Ising Hamiltonian
    print("[Converter]: Step B: Converting the QUBO to an Ising Hamiltonian...")
    # We can call .to_ising() on 'qp_unconstrained'.
    try:
        hamiltonian, offset = qp_unconstrained.to_ising()
    except Exception as e:
        print(f"\nFATAL ERROR: Error while converting problem to .to_ising(): {e}")
        return None, 0.0
    
    print("[Converter]: Conversion complete.")
    
    # Return the Hamiltonian and offset
    return hamiltonian, offset

# --- "Testing Block" ---
# This code only runs when you execute this file directly.
if __name__ == "__main__":
    
    print("\n---------------------------------------------------------")
    print(">>> 'hamiltonian_converter.py' was RUN DIRECTLY (Testing Mode) <<<")
    print("---------------------------------------------------------")
    
    # To run this test we need to run the full pipeline:
    
    # --- Imports (depending on your file structure) ---
    try:
        from data_pipeline import fetch_stock_data, calculate_mu_and_sigma
        print("Note: Imported 'data_pipeline.py'.")
    except ImportError:
        print("FATAL ERROR: 'data_pipeline.py' file not found. Cannot run test.")
        exit()

    try:
        from problem_builder import create_quadratic_program
        print("Note: Imported 'problem_builder.py'.")
    except ImportError:
        print("FATAL ERROR: 'problem_builder.py' file not found. Cannot run test.")
        exit()

    # --- Step 1: Data Laana  ---
    print("\n--- [Test Run] Step 1: Data Laana ---")
    tickers_mvp = ['AAPL', 'GOOG', 'MSFT', 'AMZN'] # n=4
    start_date = '2021-01-01'
    end_date = '2023-12-31'
    
    prices = fetch_stock_data(tickers=tickers_mvp, start_date=start_date, end_date=end_date)
    
    if prices is not None and not prices.empty:
        mu, sigma = calculate_mu_and_sigma(prices)
        
        # --- Step 2: Problem Banana  ---
        print("\n--- [Test Run] Step 2: Qiskit Problem Banana (Objective + Constraint) ---")
        k_budget = 2 # k=2
        q_risk = 1.0 # q=1
        
        qp_problem = create_quadratic_program(mu, sigma, k=k_budget, q=q_risk)
        
        # --- Step 3: Hamiltonian Convert Karna  ---
        print("\n--- [Test Run] Step 3: Ising Hamiltonian Banana (QUBO -> Ising) ---")
        
        # Call the updated conversion function
        hamiltonian, offset = convert_to_ising(qp_problem)
        
        # --- Step 4: Show Result ---
        if hamiltonian is not None:
            print("\n--- [Test Run] Result: Final Ising Hamiltonian ---")
            print("This Hamiltonian (H) is the main input for QAOA.")
            print(hamiltonian)
            print(f"\nOffset (energy constant): {offset}")
        else:
            print("Test Run Failed: Hamiltonian conversion did not succeed.")
        
    else:
        print("Test Run Failed: No data retrieved.")
# ...existing code...