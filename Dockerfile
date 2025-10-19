FROM python:3.11-slim

# Set the working directory inside the container to /app
# This is where my code will live
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install the python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Command to run the worker when the container starts
CMD ["python", "worker.py"]
