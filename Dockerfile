FROM python:3.11-slim

# Set system environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements and install dependencies cleanly
COPY modbus_lab_projects/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything (including your monitor script and modbus projects)
COPY . .

# Expose the Modbus TCP port
EXPOSE 5020

# Default command remains your workspace monitor agent
CMD ["python", "work_space_monitor.py"]
