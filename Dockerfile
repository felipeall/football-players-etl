FROM python:3.11-slim as build

ENV PIP_DEFAULT_TIMEOUT=100 \
    # Allow statements and log messages to immediately appear
    PYTHONUNBUFFERED=1 \
    # Disable a pip version check to reduce run-time & log-spam
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # Cache is useless in docker image, so disable to reduce image size
    PIP_NO_CACHE_DIR=1 \
    # Set the Poetry version to be installed
    POETRY_VERSION=1.3.2

WORKDIR /app
COPY pyproject.toml poetry.lock ./

# Install Poetry and export the dependencies
RUN pip install "poetry==$POETRY_VERSION" && \
    poetry install --no-root --no-ansi --no-interaction && \
    poetry export -f requirements.txt -o requirements.txt

FROM apache/airflow:slim-2.5.1-python3.9

COPY --from=build /app/requirements.txt .

# Set the root user
USER root

# Upgrade the package index and install security upgrades
RUN set -ex && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get upgrade -y

# Clean up
RUN set -ex && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

# Set the user to run the application
USER airflow

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --force --no-cache-dir -r requirements.txt