# Finance Calculator Full Stack Application

This project is a full-stack financial calculator with a Python Flask backend and a ReactJS frontend, containerized using Docker and orchestrated with Docker Compose.

## Features

- **Backend API (`finance_calculator` directory):**
    - Calculate Future Value (FV) of an investment.
    - Calculate Present Value (PV) required.
    - Calculate Investment Growth Rate.
    - Calculate Time to Reach a Financial Goal.
    - Exposes calculations via a RESTful API.
- **Frontend UI (`frontend` directory):**
    - User-friendly interface built with React.
    - Forms for each calculation type.
    - Communicates with the backend API to perform calculations and display results.

## Project Structure

```
.
├── docker-compose.yml
├── finance_calculator/       # Python Flask Backend
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── src/
│   │   ├── __init__.py
│   │   ├── app.py           # Flask API application
│   │   └── calculator.py    # Core calculation logic
│   └── tests/
│       ├── __init__.py
│       └── test_calculator.py
├── frontend/                 # ReactJS Frontend
│   ├── Dockerfile
│   ├── nginx.conf           # Nginx config for serving React app
│   ├── package.json
│   ├── public/
│   └── src/
│       ├── App.js           # Main React component
│       ├── index.js         # React entry point
│       └── ... (other React files)
└── README.md                 # This file
```

## Prerequisites

- Docker
- Docker Compose (v2 CLI plugin or standalone v1)

## Getting Started (Local Development)

1.  **Clone the repository (if applicable).**
2.  **Navigate to the project root directory** (where `docker-compose.yml` is located).
3.  **Build and run the application using Docker Compose:**
    ```bash
    docker compose up --build -d
    ```
    - The `-d` flag runs the containers in detached mode.
    - The first build might take some time as it downloads base images and installs dependencies.

4.  **Access the application:**
    -   Frontend UI: `http://localhost:3000`
    -   Backend API: `http://localhost:5001` (e.g., `http://localhost:5001/api/fv` for the future value endpoint)

5.  **To stop the application:**
    ```bash
    docker compose down
    ```

6.  **To view logs:**
    ```bash
    docker compose logs -f
    # Or for specific services:
    # docker compose logs -f frontend
    # docker compose logs -f backend
    ```

## Backend API Endpoints

The backend API is served from the `backend` service, typically on `http://localhost:5001`. All endpoints expect JSON requests and return JSON responses.

-   **`POST /api/fv`**: Calculate Future Value
    -   Payload: `{ "principal": float, "rate": float, "time": float, "contributions": float (optional, default 0) }`
    -   Success Response: `{ "result": float }`
-   **`POST /api/pv`**: Calculate Present Value
    -   Payload: `{ "future_value_target": float, "rate": float, "time": float }`
    -   Success Response: `{ "result": float }`
-   **`POST /api/growth_rate`**: Calculate Investment Growth Rate
    -   Payload: `{ "present_value": float, "future_value": float, "time": float }`
    -   Success Response: `{ "result": float (decimal rate) }`
-   **`POST /api/time_to_goal`**: Calculate Time to Reach Goal
    -   Payload: `{ "principal": float, "rate": float, "future_value_target": float, "contributions": float (optional, default 0) }`
    -   Success Response: `{ "result": float (years) }`

-   Error Response (example): `{ "error": "Error message details" }` (HTTP status codes 400 or 500)

## Running Backend Tests

The backend unit tests are located in `finance_calculator/tests/`.
Due to historical environment issues during development of the test execution, running them directly via `python -m unittest ...` was problematic.

If your environment is set up correctly for Python development (and you have the dependencies from `finance_calculator/requirements.txt` installed in your environment), you might be able to run them from the `finance_calculator` directory:
```bash
# Navigate to finance_calculator directory
# cd finance_calculator
# Ensure Python environment is active with dependencies installed
# Attempt to run tests (discovery from parent of 'tests' or by specifying module)
python -m unittest discover -s tests -p 'test_*.py'
```
Alternatively, you can execute tests inside the running backend Docker container:
```bash
docker compose exec backend python -m unittest discover -s tests -p 'test_*.py'
# This assumes the WORKDIR is /app and 'tests' is directly under it.
```
The backend Dockerfile has been updated to copy the `tests` directory into the image.

## Deployment to Digital Ocean (Guidance)

Refer to the detailed deployment strategy provided previously (or in a separate `DEPLOYMENT.md` if this section grows too large). Key steps include:
1.  Provisioning a Droplet.
2.  Setting up Docker and Docker Compose on the Droplet.
3.  Transferring project files (or cloning from Git).
4.  Running `docker compose up --build -d`.
5.  Configuring a firewall.
6.  (Recommended for Production) Setting up a domain, a reverse proxy (like Nginx or Traefik), and SSL/TLS certificates (e.g., with Let's Encrypt).

## Building Individual Docker Images (Optional)

If you need to build images separately without Docker Compose:

-   **Frontend:**
    ```bash
    cd frontend
    docker build -t finance-calculator-frontend:latest .
    ```
-   **Backend:**
    ```bash
    cd finance_calculator
    docker build -t finance-calculator-backend:latest .
    ```

This `README.md` provides a comprehensive overview.
The old `finance_calculator/README.md` should now be deleted.
```
