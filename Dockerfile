FROM apache/airflow:slim-2.5.1-python3.9

COPY poetry.lock pyproject.toml ./

USER airflow
RUN pip install --no-cache-dir --upgrade pip && \
    pip install poetry && \
    poetry export -o requirements.txt --without-hashes && \
    pip install -r requirements.txt