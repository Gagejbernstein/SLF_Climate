FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["solara", "run", "SSP.py", "--host", "0.0.0.0", "--port", "7860"]