FROM python:3.10-slim

WORKDIR /app

# Install uv to manage Python packages
RUN pip install --no-cache-dir uv

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN uv pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create a non-root user to run the application
RUN useradd -m merakiuser
USER merakiuser

# Set environment variable
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["uv", "run", "meraki_server.py"]
