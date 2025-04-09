# Use a minimal base image with Python
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
        build-essential \
        gdal-bin \
        libgdal-dev \
        curl \
        && rm -rf /var/lib/apt/lists/*

# Install pip and wheel
RUN pip install --upgrade pip && pip install wheel

# Copy app code into the container
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Run the Solara app
CMD ["solara", "run", "SSP.py", "--host", "0.0.0.0", "--port", "10000"]
