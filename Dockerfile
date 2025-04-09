# Use slim Python 3.10 base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files into the container
COPY . /app

# Upgrade pip, install wheel early to prevent bdist_wheel errors
RUN pip install --upgrade pip \
 && pip install wheel \
 && pip install -r requirements.txt

# Expose the port your app runs on (default Solara port is 8765)
EXPOSE 8765

# Default command to run the Solara app
CMD ["solara", "run", "SSP.py", "--host", "0.0.0.0", "--port", "8765"]
