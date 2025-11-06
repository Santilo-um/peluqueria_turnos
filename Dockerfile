FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

COPY . .

ENV FLASK_APP=run.py
ENV FLASK_ENV=development
ENV PYTHONPATH=/app
