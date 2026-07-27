# --- Stage explanation ---
# We use a "slim" Python base image instead of the full image to keep the
# final container small (faster pulls, smaller attack surface).
FROM python:3.11-slim

# Prevents Python from writing .pyc files and buffers output — makes logs
# appear immediately in `docker logs` instead of being buffered.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a non-root user. Running containers as root is a common security
# mistake — if the app is ever compromised, a non-root user limits damage.
RUN useradd --create-home appuser
WORKDIR /app

# Copy only requirements.txt first, THEN install. Docker caches each layer
# by its inputs — this means "pip install" only re-runs when
# requirements.txt actually changes, not on every code edit, which makes
# rebuilds during development much faster.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the application code.
COPY . .

# Ensure the logs directory exists and is writable by the non-root user.
RUN mkdir -p logs && chown -R appuser:appuser /app

USER appuser

# Default command: run continuously (polling mode).
CMD ["python", "main.py"]
