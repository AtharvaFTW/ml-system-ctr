FROM apache/airflow:3.2.2
COPY docker/requirements.txt /docker-requirements.txt
RUN pip install uv
RUN uv pip install --no-cache-dir -r /docker-requirements.txt
