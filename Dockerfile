FROM python:3.10-slim

# Install system packages
RUN apt-get update && apt-get install -y \
    git build-essential libgdal-dev gdal-bin \
    && rm -rf /var/lib/apt/lists/*

# Install pip packages
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Add the app code
COPY app /app
WORKDIR /app

# Expose Solara on port 7860
CMD ["solara", "run", "SSP.py", "--host", "0.0.0.0", "--port", "7860"]
