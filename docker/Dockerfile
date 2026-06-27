FROM apache/airflow:3.2.2
COPY requirements.txt .
RUN pip install uv
RUN uv pip install --no-cache-dir -r requirements.txt
RUN uv pip install "structlog==25.5.0"