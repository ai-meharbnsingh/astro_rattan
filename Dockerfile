FROM python:3.12-slim
WORKDIR /app

# System packages:
#   - gcc/g++/make: build pyswisseph
#   - tesseract-ocr: OCR for Vastu floor plan room detection
#   - libgl1 + libglib2.0-0: OpenCV headless runtime deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ python3-dev make \
    tesseract-ocr \
    libgl1 libglib2.0-0 && \
    pip install --no-cache-dir pyswisseph && \
    apt-get purge -y gcc g++ python3-dev make && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Swiss Ephemeris — use Moshier (built-in, no download needed)
# Accuracy: ~0.5 arcminute. For arc-second precision, mount .se1 files at /usr/share/swisseph/ephe
RUN mkdir -p /usr/share/swisseph/ephe
ENV EPHE_PATH=/usr/share/swisseph/ephe

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ app/
COPY static/ static/
EXPOSE 8028
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8028} --workers ${WEB_CONCURRENCY:-4}
