FROM python:3.10-slim

WORKDIR /app

RUN pip install --upgrade pip && pip install wheel

COPY . /app

# Prevent pyperclip from being installed
RUN pip install -r requirements.txt -c constraints.txt

CMD ["solara", "run", "SSP.py", "--host", "0.0.0.0", "--port", "7860"]
