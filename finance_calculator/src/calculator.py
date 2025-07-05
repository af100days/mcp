"""
Core financial calculation functions for investments.

Provides functions for:
- Future Value (FV)
- Present Value (PV)
- Investment Growth Rate
- Time to Reach Financial Goal
"""
import math

def future_value(principal: float, rate: float, time: float, contributions: float = 0) -> float:
    """
    Calculates the future value of an investment with optional regular contributions.

    Args:
        principal: The initial principal amount.
        rate: The annual interest rate (as a decimal, e.g., 0.05 for 5%).
        time: The number of years the money is invested for.
        contributions: The amount of regular contributions made each year (optional).

    Returns:
        The future value of the investment.
    """
    if contributions == 0:
        return principal * (1 + rate) ** time
    else:
        # Future value of principal
        fv_principal = principal * (1 + rate) ** time
        # Future value of a series of contributions
        fv_contributions = contributions * (((1 + rate) ** time - 1) / rate)
        return fv_principal + fv_contributions

def present_value(future_value_target: float, rate: float, time: float) -> float:
    """
    Calculates the present value needed to reach a future value target.

    Args:
        future_value_target: The desired future value.
        rate: The annual discount rate (as a decimal).
        time: The number of years.

    Returns:
        The present value required.
    """
    return future_value_target / ((1 + rate) ** time)

def investment_growth_rate(present_value_amount: float, future_value_target: float, time: float) -> float:
    """
    Calculates the annual growth rate of an investment.

    Args:
        present_value_amount: The initial value of the investment.
        future_value_target: The future value of the investment.
        time: The number of years.

    Returns:
        The annual growth rate (as a decimal).
    """
    if present_value_amount <= 0:
        raise ValueError("Present value must be positive to calculate growth rate.")
    return (future_value_target / present_value_amount) ** (1 / time) - 1

def time_to_reach_goal(principal: float, rate: float, future_value_target: float, contributions: float = 0) -> float:
    """
    Calculates the time (in years) to reach a financial goal.

    Args:
        principal: The initial principal amount.
        rate: The annual interest rate (as a decimal).
        future_value_target: The desired future value.
        contributions: The amount of regular contributions made each year (optional).

    Returns:
        The number of years to reach the goal.
    """
    if rate <= 0:
        raise ValueError("Interest rate must be positive to calculate time to goal.")
    if future_value_target <= principal and contributions <=0:
        return 0 # Goal is already met or no growth possible

    # Using logarithms to solve for t in FV formulas
    # If no contributions: FV = PV * (1+r)^t  => t = log(FV/PV) / log(1+r)
    if contributions == 0:
        if future_value_target <= principal: # Should be caught above, but as a safeguard
            return 0
        if principal <= 0 : # Cannot reach a positive FV from 0 or negative PV without contributions
            return float('inf') # Or raise error
        return math.log(future_value_target / principal) / math.log(1 + rate)
    else:
        # This is more complex: FV = PV*(1+r)^t + C*[((1+r)^t - 1)/r]
        # No simple algebraic solution for t. We can use an iterative approach or a financial library.
        # For simplicity in this initial skeleton, we'll use an iterative approach.
        # This is a placeholder for a more robust solution, perhaps using `scipy.optimize.fsolve` or similar.
        years = 0
        current_value = principal
        max_years = 1000 # Safety break for the loop
        while current_value < future_value_target and years < max_years:
            current_value = current_value * (1 + rate) + contributions
            years += 1
        return years if current_value >= future_value_target else float('inf')
