FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN apt update && apt install libpq-dev gcc -y && pip install -r requirements.txt && rm -rf /var/lib/apt/lists/*
COPY . .
CMD ["python", "app.py"]