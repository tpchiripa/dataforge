FROM apache/airflow:3.0.2-python3.12

USER root

RUN apt-get update && apt-get install -y \
    git \
    curl \
    vim \
    build-essential \
    && apt-get clean

USER airflow

RUN pip install --no-cache-dir \
    psycopg2-binary \
    redis \
    pandas \
    pyarrow \
    sqlalchemy
    FROM apache/airflow:3.0.2-python3.12

USER root

RUN apt-get update && apt-get install -y \
    git \
    curl \
    vim \
    build-essential \
    && apt-get clean

USER airflow

RUN pip install --no-cache-dir \
    pandas \
    pyarrow \
    redis \
    boto3 \
    psycopg2-binary
