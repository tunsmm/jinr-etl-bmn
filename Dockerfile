FROM apache/airflow:2.8.3-python3.11

COPY ./app/requirements.txt /opt/airflow/requirements.txt

# Устанавливаем зависимости от airflow и возвращаемся к root
USER airflow
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

USER root
