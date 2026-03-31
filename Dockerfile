# Dockerfile
FROM python:3.11-slim-bookworm

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip setuptools wheel --default-timeout=300
RUN pip install --no-cache-dir --default-timeout=300 -r requirements.txt

COPY . .

RUN mkdir -p /app/temp /app/logs
RUN chmod 777 /app/temp /app/logs

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]