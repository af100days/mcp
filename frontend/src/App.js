import React, { useState } from 'react';
import './App.css';

function App() {
  // For now, a simple placeholder.
  // We will build out forms and logic here.
  const [calculationType, setCalculationType] = useState('fv');
  const [result, setResult] = useState(null);

  // Placeholder for form inputs
  const [principal, setPrincipal] = useState('');
  const [rate, setRate] = useState('');
  const [time, setTime] = useState('');
  const [contributions, setContributions] = useState('');
  const [futureValueTarget, setFutureValueTarget] = useState('');
  const API_BASE_URL = 'http://localhost:5001/api'; // Backend API URL

  // Form states
  const [calculationType, setCalculationType] = useState('fv');

  // Universal inputs where applicable
  const [principal, setPrincipal] = useState('');
  const [rate, setRate] = useState('');
  const [time, setTime] = useState('');
  const [contributions, setContributions] = useState(''); // Optional for FV and TimeToGoal
  const [futureValue, setFutureValue] = useState(''); // Used as target for PV, actual for Growth Rate
  const [presentValue, setPresentValue] = useState(''); // Used for Growth Rate

  // Output state
  const [apiResult, setApiResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const clearInputs = () => {
    setPrincipal('');
    setRate('');
    setTime('');
    setContributions('');
    setFutureValue('');
    setPresentValue('');
    setApiResult(null);
    setError(null);
  };

  const handleCalculationTypeChange = (e) => {
    setCalculationType(e.target.value);
    clearInputs(); // Clear inputs when changing calculation type
  };

  const handleCalculate = async () => {
    setLoading(true);
    setError(null);
    setApiResult(null);

    let payload = {};
    let endpoint = '';

    switch (calculationType) {
      case 'fv':
        payload = {
          principal: parseFloat(principal),
          rate: parseFloat(rate),
          time: parseFloat(time),
          contributions: contributions ? parseFloat(contributions) : 0
        };
        endpoint = '/fv';
        break;
      case 'pv':
        payload = {
          future_value_target: parseFloat(futureValue),
          rate: parseFloat(rate),
          time: parseFloat(time)
        };
        endpoint = '/pv';
        break;
      case 'growth_rate':
        payload = {
          present_value: parseFloat(presentValue),
          future_value: parseFloat(futureValue),
          time: parseFloat(time)
        };
        endpoint = '/growth_rate';
        break;
      case 'time_to_goal':
        payload = {
          principal: parseFloat(principal),
          rate: parseFloat(rate),
          future_value_target: parseFloat(futureValue),
          contributions: contributions ? parseFloat(contributions) : 0
        };
        endpoint = '/time_to_goal';
        break;
      default:
        setError("Invalid calculation type selected.");
        setLoading(false);
        return;
    }

    // Basic NaN validation after parseFloat
    for (const key in payload) {
        if (isNaN(payload[key])) {
            setError(`Invalid input for ${key}. Please enter valid numbers.`);
            setLoading(false);
            return;
        }
    }

    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (!response.ok) {
        setError(data.error || `API Error: ${response.status}`);
      } else {
        setApiResult(data.result);
      }
    } catch (err) {
      setError(`Network or fetch error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const renderFormFields = () => {
    switch (calculationType) {
      case 'fv':
        return (
          <>
            <input type="number" value={principal} onChange={(e) => setPrincipal(e.target.value)} placeholder="Principal" />
            <input type="number" step="0.001" value={rate} onChange={(e) => setRate(e.target.value)} placeholder="Annual Rate (e.g., 0.05)" />
            <input type="number" value={time} onChange={(e) => setTime(e.target.value)} placeholder="Time (years)" />
            <input type="number" value={contributions} onChange={(e) => setContributions(e.target.value)} placeholder="Annual Contributions (optional)" />
          </>
        );
      case 'pv':
        return (
          <>
            <input type="number" value={futureValue} onChange={(e) => setFutureValue(e.target.value)} placeholder="Future Value Target" />
            <input type="number" step="0.001" value={rate} onChange={(e) => setRate(e.target.value)} placeholder="Annual Discount Rate (e.g., 0.05)" />
            <input type="number" value={time} onChange={(e) => setTime(e.target.value)} placeholder="Time (years)" />
          </>
        );
      case 'growth_rate':
        return (
          <>
            <input type="number" value={presentValue} onChange={(e) => setPresentValue(e.target.value)} placeholder="Present Value" />
            <input type="number" value={futureValue} onChange={(e) => setFutureValue(e.target.value)} placeholder="Future Value" />
            <input type="number" value={time} onChange={(e) => setTime(e.target.value)} placeholder="Time (years)" />
          </>
        );
      case 'time_to_goal':
        return (
          <>
            <input type="number" value={principal} onChange={(e) => setPrincipal(e.target.value)} placeholder="Principal" />
            <input type="number" step="0.001" value={rate} onChange={(e) => setRate(e.target.value)} placeholder="Annual Rate (e.g., 0.05)" />
            <input type="number" value={futureValue} onChange={(e) => setFutureValue(e.target.value)} placeholder="Future Value Target" />
            <input type="number" value={contributions} onChange={(e) => setContributions(e.target.value)} placeholder="Annual Contributions (optional)" />
          </>
        );
      default:
        return null;
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Finance Calculator</h1>
      </header>
      <main>
        <div>
          <label htmlFor="calcType">Select Calculation: </label>
          <select id="calcType" value={calculationType} onChange={handleCalculationTypeChange}>
            <option value="fv">Future Value (FV)</option>
            <option value="pv">Present Value (PV)</option>
            <option value="growth_rate">Investment Growth Rate</option>
            <option value="time_to_goal">Time to Reach Goal</option>
          </select>
        </div>

        <div className="form-fields">
          {renderFormFields()}
        </div>

        <button onClick={handleCalculate} disabled={loading}>
          {loading ? 'Calculating...' : 'Calculate'}
        </button>

        {error && (
          <div className="error-message">
            <h3>Error:</h3>
            <p>{error}</p>
          </div>
        )}

        {apiResult !== null && !error && (
          <div className="result">
            <h3>Result:</h3>
            <pre>
              {calculationType === 'growth_rate'
                ? `${(apiResult * 100).toFixed(2)}%`
                : typeof apiResult === 'number'
                  ? apiResult.toFixed(2)
                  : JSON.stringify(apiResult, null, 2)}
              {calculationType === 'time_to_goal' && apiResult !== Infinity && apiResult !== 0 ? ' years' : ''}
            </pre>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
