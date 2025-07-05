"""
Command-line interface for the Financial Calculator.

This script uses argparse to provide a CLI for accessing the financial
calculations defined in the 'calculator' module.
"""
import argparse
from . import calculator # Use relative import

def main():
    parser = argparse.ArgumentParser(description="Financial Calculator MCP")
    subparsers = parser.add_subparsers(dest="command", help="Available calculations", required=True)

    # Future Value
    fv_parser = subparsers.add_parser("fv", help="Calculate Future Value")
    fv_parser.add_argument("principal", type=float, help="Initial principal amount")
    fv_parser.add_argument("rate", type=float, help="Annual interest rate (e.g., 0.05 for 5%)")
    fv_parser.add_argument("time", type=float, help="Number of years")
    fv_parser.add_argument("--contributions", type=float, default=0, help="Annual contributions (optional)")

    # Present Value
    pv_parser = subparsers.add_parser("pv", help="Calculate Present Value")
    pv_parser.add_argument("future_value", type=float, help="Desired future value")
    pv_parser.add_argument("rate", type=float, help="Annual discount rate (e.g., 0.05 for 5%)")
    pv_parser.add_argument("time", type=float, help="Number of years")

    # Investment Growth Rate
    rate_parser = subparsers.add_parser("growth_rate", help="Calculate Investment Growth Rate")
    rate_parser.add_argument("present_value", type=float, help="Initial investment value")
    rate_parser.add_argument("future_value", type=float, help="Future investment value")
    rate_parser.add_argument("time", type=float, help="Number of years")

    # Time to Reach Goal
    time_parser = subparsers.add_parser("time_to_goal", help="Calculate Time to Reach Financial Goal")
    time_parser.add_argument("principal", type=float, help="Initial principal amount")
    time_parser.add_argument("rate", type=float, help="Annual interest rate (e.g., 0.05 for 5%)")
    time_parser.add_argument("future_value_target", type=float, help="Desired future value")
    time_parser.add_argument("--contributions", type=float, default=0, help="Annual contributions (optional)")

    args = parser.parse_args()

    result = None
    try:
        if args.command == "fv":
            result = calculator.future_value(args.principal, args.rate, args.time, args.contributions)
            print(f"Future Value: {result:.2f}")
        elif args.command == "pv":
            result = calculator.present_value(args.future_value, args.rate, args.time)
            print(f"Present Value needed: {result:.2f}")
        elif args.command == "growth_rate":
            result = calculator.investment_growth_rate(args.present_value, args.future_value, args.time)
            print(f"Required Annual Growth Rate: {result*100:.2f}%")
        elif args.command == "time_to_goal":
            result = calculator.time_to_reach_goal(args.principal, args.rate, args.future_value_target, args.contributions)
            if result == float('inf'):
                print("Goal may not be reachable under the given conditions or will take a very long time.")
            elif result == 0 and args.future_value_target <= args.principal and args.contributions <=0 :
                 print("Goal is already met or exceeded, or no growth is possible with current inputs.")
            elif result == 0 and args.future_value_target > args.principal : # Should not happen if logic in calculator is correct
                 print("Goal is already met or exceeded.")
            else:
                print(f"Time to reach financial goal: {result:.2f} years")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
