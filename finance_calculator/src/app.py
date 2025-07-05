"""
Flask API for the Financial Calculator.

Exposes the financial calculation functions from 'calculator.py'
as HTTP endpoints.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from . import calculator # Use relative import for sibling module

app = Flask(__name__)
CORS(app) # Enable CORS for all routes, allowing requests from the React frontend

@app.route('/')
def hello():
    return jsonify(message="Finance Calculator API is running!")

@app.route('/api/fv', methods=['POST'])
def future_value_api():
    data = request.get_json()
    if not data:
        return jsonify(error="Invalid input: No JSON data received"), 400

    principal = data.get('principal')
    rate = data.get('rate')
    time = data.get('time')
    contributions = data.get('contributions', 0) # Optional

    if None in [principal, rate, time]:
        return jsonify(error="Missing required fields: principal, rate, time"), 400

    try:
        principal = float(principal)
        rate = float(rate)
        time = float(time)
        contributions = float(contributions)
        if rate < 0 or time < 0 or principal < 0 or contributions < 0 :
             if contributions < 0 and principal - contributions < 0 : # allow for withdrawals if principal can cover
                pass # allow if principal can cover withdrawals initially
             else:
                return jsonify(error="Principal, rate, time, and contributions cannot be negative (unless contributions are withdrawals covered by principal)"), 400


        result = calculator.future_value(principal, rate, time, contributions)
        return jsonify(result=result)
    except ValueError as e:
        return jsonify(error=str(e)), 400
    except Exception as e:
        return jsonify(error=f"An unexpected error occurred: {str(e)}"), 500

@app.route('/api/pv', methods=['POST'])
def present_value_api():
    data = request.get_json()
    if not data:
        return jsonify(error="Invalid input: No JSON data received"), 400

    future_value_target = data.get('future_value_target')
    rate = data.get('rate')
    time = data.get('time')

    if None in [future_value_target, rate, time]:
        return jsonify(error="Missing required fields: future_value_target, rate, time"), 400

    try:
        future_value_target = float(future_value_target)
        rate = float(rate)
        time = float(time)
        if rate <= 0 or time <= 0 : # Rate must be positive for discounting, time must be positive
            return jsonify(error="Rate and time must be positive for present value calculation"), 400


        result = calculator.present_value(future_value_target, rate, time)
        return jsonify(result=result)
    except ValueError as e:
        return jsonify(error=str(e)), 400
    except Exception as e:
        return jsonify(error=f"An unexpected error occurred: {str(e)}"), 500

@app.route('/api/growth_rate', methods=['POST'])
def growth_rate_api():
    data = request.get_json()
    if not data:
        return jsonify(error="Invalid input: No JSON data received"), 400

    present_value_amount = data.get('present_value')
    future_value_target = data.get('future_value')
    time = data.get('time')

    if None in [present_value_amount, future_value_target, time]:
        return jsonify(error="Missing required fields: present_value, future_value, time"), 400

    try:
        present_value_amount = float(present_value_amount)
        future_value_target = float(future_value_target)
        time = float(time)
        # calculator.investment_growth_rate already raises ValueError for present_value_amount <= 0
        # and time <=0 would lead to division by zero or meaningless result in (1/time)
        if time <= 0:
            return jsonify(error="Time must be positive for growth rate calculation"), 400

        result = calculator.investment_growth_rate(present_value_amount, future_value_target, time)
        return jsonify(result=result)
    except ValueError as e:
        return jsonify(error=str(e)), 400 # Catches issues from calculator.py like PV <= 0
    except Exception as e:
        return jsonify(error=f"An unexpected error occurred: {str(e)}"), 500

@app.route('/api/time_to_goal', methods=['POST'])
def time_to_goal_api():
    data = request.get_json()
    if not data:
        return jsonify(error="Invalid input: No JSON data received"), 400

    principal = data.get('principal')
    rate = data.get('rate')
    future_value_target = data.get('future_value_target')
    contributions = data.get('contributions', 0) # Optional

    if None in [principal, rate, future_value_target]:
        return jsonify(error="Missing required fields: principal, rate, future_value_target"), 400

    try:
        principal = float(principal)
        rate = float(rate)
        future_value_target = float(future_value_target)
        contributions = float(contributions)

        # calculator.time_to_reach_goal raises ValueError for rate <= 0
        # Other checks like principal vs future_value_target are handled by the calculator logic

        result = calculator.time_to_reach_goal(principal, rate, future_value_target, contributions)
        return jsonify(result=result)
    except ValueError as e:
        return jsonify(error=str(e)), 400 # Catches issues from calculator.py like rate <=0
    except Exception as e:
        return jsonify(error=f"An unexpected error occurred: {str(e)}"), 500

if __name__ == '__main__':
    # This is for local development running `python -m finance_calculator.src.app`
    # For production, a WSGI server like Gunicorn will be used.
    app.run(debug=True, host='0.0.0.0', port=5001) # Using port 5001 for backend API
