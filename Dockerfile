FROM python:3.10-slim-bullseye

WORKDIR /app

# Set environment to bypass SSL issues
ENV PYTHONWARNINGS="ignore:Unverified HTTPS request"
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies without uv, using pip directly with SSL bypass
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt || \
    (pip config set global.index-url https://pypi.org/simple && \
     pip config set global.trusted-host "pypi.org files.pythonhosted.org" && \
     pip install --no-cache-dir -r requirements.txt)

# Copy the rest of the application
COPY . .

# Create a non-root user to run the application
RUN useradd -m merakiuser
USER merakiuser

# Set environment variable
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["python", "http_server.py"]
