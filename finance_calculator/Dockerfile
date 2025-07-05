# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the src directory and its contents into the container at /app/src
COPY src ./src
# Copy the tests directory
COPY tests ./tests

# Make port 5001 available to the world outside this container
# Gunicorn will bind to this port.
EXPOSE 5001

# Define environment variables (optional for Gunicorn if specified in CMD)
ENV FLASK_APP=src.app:app
# FLASK_APP should point to the file and then the Flask app instance.
# Since app.py is in src, and the Flask instance is 'app'.

# Run app.py when the container launches using Gunicorn
# The module is src.app, and the Flask app instance is 'app'
# Bind to 0.0.0.0 to be accessible from outside the container.
# The number of workers can be adjusted based on CPU cores, e.g., (2 * CPU_CORES) + 1
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:5001", "src.app:app"]
