# TechStore support agent: the Streamlit demo plus the CLI tools.
#   docker compose up --build          (from the repo root)  ->  http://localhost:8501
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/opt/hf

WORKDIR /app

# CPU-only torch first: the default wheel bundles CUDA (~2 GB) we never use.
RUN pip install --index-url https://download.pytorch.org/whl/cpu torch
COPY requirements.txt .
RUN pip install -r requirements.txt

# Download MiniLM at build time so the container starts offline and fast.
RUN python -c "from sentence_transformers import SentenceTransformer; \
SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', device='cpu')" \
 && chmod -R a+rX /opt/hf

COPY . .
RUN useradd --create-home app && chown -R app /app
USER app
ENV HF_HUB_OFFLINE=1

EXPOSE 8501
HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')"

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501", \
     "--server.headless=true", "--browser.gatherUsageStats=false"]
