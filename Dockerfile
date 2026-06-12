# A container image so the app runs the same everywhere.
# The CD workflow builds this image as the "deployment artifact".
FROM python:3.12-slim

WORKDIR /app

# Install dependencies first so Docker can cache this layer.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code.
COPY app/ ./app/

EXPOSE 5000

# gunicorn is a production-grade server (Flask's built-in one is dev-only).
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.main:app"]
