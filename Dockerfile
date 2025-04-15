# Dockerfile
FROM python:3.10-slim

ENV GOOGLE_API_KEY="AIzaSyCMm3lgZTAgIF3oaG_jjvEiSFtFJCHEtHo"

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
