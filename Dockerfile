FROM python:3.12-slim
WORKDIR /app

# Install build dependencies for pyswisseph (Swiss Ephemeris C/C++ extension)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ python3-dev make && \
    pip install --no-cache-dir pyswisseph && \
    apt-get purge -y gcc g++ python3-dev make && \
    apt-get autoremove -y && \
    apt-get clean

# Download Swiss Ephemeris data files for arc-second precision
# sepl*.se1 = planet ephemeris, semo*.se1 = moon, seas*.se1 = asteroids
RUN apt-get update && apt-get install -y --no-install-recommends wget && \
    mkdir -p /usr/share/swisseph/ephe && cd /usr/share/swisseph/ephe && \
    wget -q https://www.astro.com/ftp/swisseph/ephe/sepl_18.se1 && \
    wget -q https://www.astro.com/ftp/swisseph/ephe/semo_18.se1 && \
    wget -q https://www.astro.com/ftp/swisseph/ephe/seas_18.se1 && \
    apt-get purge -y wget && apt-get autoremove -y && apt-get clean
ENV EPHE_PATH=/usr/share/swisseph/ephe

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ app/
COPY static/ static/
EXPOSE 8080
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080} --workers ${WEB_CONCURRENCY:-2}
