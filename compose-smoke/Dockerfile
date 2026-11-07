FROM python:3.13.11-alpine3.23
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONPATH=/app
WORKDIR /app
COPY calculator.py /app/calculator.py
COPY compose-smoke/api.py /app/api.py
RUN mkdir /data
CMD ["python", "/app/api.py"]
