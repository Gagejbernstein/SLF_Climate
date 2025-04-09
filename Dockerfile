FROM python:3.10-slim

WORKDIR /app

COPY . /app

# Upgrade pip and install wheel first
RUN pip install --upgrade pip \
 && pip install wheel

# Then install the rest of the dependencies
RUN pip install -r requirements.txt

CMD ["solara", "run", "main.py", "--host", "0.0.0.0", "--port", "7860"]
