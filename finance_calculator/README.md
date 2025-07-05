# Finance Calculator MCP

A command-line tool for performing common financial calculations related to investments.

## Features

- Calculate Future Value (FV) of an investment, with or without regular contributions.
- Calculate Present Value (PV) required to meet a future financial goal.
- Calculate the required annual Investment Growth Rate to reach a future value from a present value over a set time.
- Calculate the Time (in years) to reach a financial goal, with or without regular contributions.

## Installation

No installation is required beyond having Python 3.x. The calculator is run directly from its source files.

## Usage

The calculator is run from the command line using Python. Navigate to the directory *containing* the `finance_calculator` project directory.

```bash
python -m finance_calculator.src.main [command] [options]
```

Alternatively, if you are inside the `finance_calculator` directory:
```bash
python -m src.main [command] [options]
```

Or, to make it directly executable (after `chmod +x finance_calculator/src/main.py` and ensuring a shebang like `#!/usr/bin/env python3` is at the top of `main.py`):
```bash
./finance_calculator/src/main.py [command] [options]
```

### Commands and Options

#### 1. Future Value (`fv`)

Calculates the future value of an investment.

**Arguments:**
- `principal`: Initial principal amount (float).
- `rate`: Annual interest rate as a decimal (e.g., 0.05 for 5%) (float).
- `time`: Number of years the money is invested for (float).
- `--contributions`: (Optional) Amount of regular annual contributions (float, defaults to 0).

**Example:**
```bash
python -m finance_calculator.src.main fv 1000 0.05 10 --contributions 100
# Output: Future Value: 2886.68
```

#### 2. Present Value (`pv`)

Calculates the present value needed to reach a future value target.

**Arguments:**
- `future_value`: The desired future value (float).
- `rate`: The annual discount rate as a decimal (e.g., 0.05 for 5%) (float).
- `time`: The number of years (float).

**Example:**
```bash
python -m finance_calculator.src.main pv 2000 0.05 10
# Output: Present Value needed: 1227.83
# (Note: Manual calculation for PV of 2000 @ 5% over 10 years is 2000 / (1.05^10) = 2000 / 1.62889 = 1227.82, my test case for PV was 1628.89 / (1.05^10) = 1000)
# Let's re-verify the example output. calculator.present_value(2000,0.05,10) -> 2000 / (1.05**10) = 1227.82649...
# Output: Present Value needed: 1227.83 (Correct)
```

#### 3. Investment Growth Rate (`growth_rate`)

Calculates the annual growth rate of an investment.

**Arguments:**
- `present_value`: The initial value of the investment (float).
- `future_value`: The future value of the investment (float).
- `time`: The number of years (float).

**Example:**
```bash
python -m finance_calculator.src.main growth_rate 1000 1628.89 10
# Output: Required Annual Growth Rate: 5.00%
```

#### 4. Time to Reach Goal (`time_to_goal`)

Calculates the time (in years) to reach a financial goal.

**Arguments:**
- `principal`: The initial principal amount (float).
- `rate`: The annual interest rate as a decimal (e.g., 0.05 for 5%) (float).
- `future_value_target`: The desired future value (float).
- `--contributions`: (Optional) Amount of regular annual contributions (float, defaults to 0).

**Example:**
```bash
python -m finance_calculator.src.main time_to_goal 1000 0.05 2000 --contributions 100
# Output: Time to reach financial goal: 6.00 years
```

### Running Tests

Unit tests are located in the `finance_calculator/tests` directory. Due to potential environment issues with `run_in_bash_session`, the recommended way to run tests (if the environment allows) is from the workspace root directory:

```bash
python -m unittest discover -s finance_calculator/tests -p 'test_*.py'
```
If this fails due to path issues, you might need to adjust Python's path or use an IDE's test runner. The tests are written using Python's `unittest` module.

## Code Structure

- `finance_calculator/src/calculator.py`: Contains the core financial calculation logic.
- `finance_calculator/src/main.py`: Provides the command-line interface.
- `finance_calculator/src/__init__.py`: Makes `src` a Python package.
- `finance_calculator/tests/test_calculator.py`: Contains unit tests for the calculator functions.
- `finance_calculator/tests/__init__.py`: Makes `tests` a Python package.
- `finance_calculator/README.md`: This file.

## Error Handling

The CLI will output error messages for invalid inputs (e.g., non-numeric values where numbers are expected, or mathematically problematic values like a zero interest rate when calculating time to goal). It will also catch unexpected errors.

## Future Improvements (Potential)

- More sophisticated solver for `time_to_reach_goal` with contributions (e.g., using a numerical method like Newton-Raphson or a library function if available, instead of simple iteration).
- Handling different compounding frequencies (e.g., monthly, quarterly). Currently assumes annual compounding and contributions.
- Adding more financial calculations (e.g., loan amortization, ROI, CAGR for a series of cash flows).
- Input validation for sensible ranges (e.g., rate > 0 for most growth calculations).
- More comprehensive error messages.
- Option for GUI or web interface.
- Packaging for easier distribution (e.g., using `setup.py`).
```
