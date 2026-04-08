FROM python:3.12-slim
WORKDIR /app

# Install build dependencies for pyswisseph (Swiss Ephemeris C/C++ extension)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ python3-dev make && \
    pip install --no-cache-dir pyswisseph && \
    apt-get purge -y gcc g++ python3-dev make && \
    apt-get autoremove -y && \
    apt-get clean

# Create ephemeris data directory (pyswisseph uses built-in Moshier ephemeris
# by default; set EPHE_PATH env var to point to Swiss Ephemeris data files
# for higher precision if available)
RUN mkdir -p /usr/share/swisseph/ephe
ENV EPHE_PATH=/usr/share/swisseph/ephe

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ app/
COPY static/ static/
EXPOSE 8080
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080} --workers ${WEB_CONCURRENCY:-2}
