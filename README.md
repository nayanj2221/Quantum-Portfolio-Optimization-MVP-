## Quantum Portfolio Optimization (MVP)
This project is a **Minimum Viable Product** (MVP) demonstrating how to solve a Mean-Variance Portfolio Optimization problem using the Quantum Approximate Optimization Algorithm (QAOA).\
This is an end-to-end Python pipeline that:
1. **Fetches Data:** Downloads real historical stock price data from Yahoo! 
2. **Finance.Calculates Inputs:** Computes the expected returns vector ($\mu$) and the covariance matrix ($\Sigma$).
3. **Defines Problem:** Uses Qiskit Optimization to build a `QuadraticProgram` representing the problem (Objective: `q*Risk - Return`, Constraint: k assets).
4. **Converts:** Translates the `QuadraticProgram` into an Ising Hamiltonian (the language of quantum).
5. **Solves:** Uses the `SamplingVQE` (as a QAOA engine) and a Qiskit Aer simulator to find the optimal solution (ground state).
6. **Outputs:** Interprets the quantum result (e.g., `'0110'`) back into a human-readable portfolio (e.g., [`'GOOG', 'MSFT'`]) and saves it to a `results.json` file.

## Project Structure
This project uses a flat file structure  for simplicity.
```
YFinace/
│
├── data_pipeline.py        # Module for Task 2: Data fetching and processing (μ, Σ)
├── problem_builder.py      # Module for Task 3.2: Building the Qiskit 'QuadraticProgram'
├── hamiltonian_converter.py # Module for Task 3.3: Converting the problem to an Ising Hamiltonian
├── qaoa_solver.py          # Module for Task 3.4: Solving the Hamiltonian with the QAOA (SamplingVQE) engine
│
├── main_project.py         # EXECUTABLE: This is the main file to run the entire pipeline
│
├── requirements.txt        # A list of all necessary Python libraries
├── .gitignore              # Tells Git which files to ignore (e.g., 'qc_env/')
├── LICENSE                 # The MIT License for the project
└── README.md               # This file

```
## How to Run
Clone the Repository:
```
git clone https://github.com/nayanj2221/Quantum-Portfolio-Optimization-MVP-
cd <your-repo-folder>
```
Create a Virtual Environment :
```
python -m venv qc_env
# On Windows
.\qc_env\Scripts\activate
# On macOS/Linux
source qc_env/bin/activate
```
### Install Required Libraries:
Install all the project dependencies from the `requirements.txt` file.
```
pip install -r requirements.txt
```
### Run the Pipeline:
Execute the main_project.py script. This will run the full end-to-end pipeline.
```
python main_project.py
```
## Example Output (results.json)
After running, the script will generate a `results.json` file with the optimal portfolio found by the quantum algorithm.
```
{
    "selected_stocks": [
        "GOOG",
        "MSFT"
    ],
    "optimal_score": -0.2156,
    "binary_solution": "0110",
    "parameters": {
        "tickers": [
            "AAPL",
            "GOOG",
            "MSFT",
            "AMZN"
        ],
        "k_budget": 2,
        "q_risk": 1.0
    },
    "raw_eigenstate_dict": {
        "0110": 0.5,
        "1001": 0.5
    },
    "total_runtime_seconds": 5.72,
    "offset": 123.456
}
```
