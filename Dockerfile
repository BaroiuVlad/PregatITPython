FROM python:3.11-slim


RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


ENV PYTHONPATH=/app/App


CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "App.api:app", "--bind", "0.0.0.0:8000"]