FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Create the logs directory and ensure it has the correct permissions
RUN mkdir -p /app/logs && chmod -R 777 /app/logs

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
