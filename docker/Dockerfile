FROM apache/airflow:3.2.2
COPY docker/requirements.txt /docker-requirements.txt
RUN pip install --no-cache-dir --no-deps feast==0.63.0
RUN pip install --no-cache-dir --no-deps -r /docker-requirements.txt --ignore-requires-python
