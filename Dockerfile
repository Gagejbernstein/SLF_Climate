FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install basic system build tools and Python build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    && pip install --upgrade pip \
    && pip install setuptools wheel

# Copy the application code
COPY . /app

# Install Python dependencies using constraints
RUN pip install -r requirements.txt -c constraints.txt

# Expose the default port for Solara
EXPOSE 8765

# Run the app
CMD ["solara", "run", "app.py", "--host", "0.0.0.0", "--port", "8765"]
