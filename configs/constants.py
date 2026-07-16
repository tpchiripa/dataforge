"""
DataForge Configuration Constants
"""

from __future__ import annotations

from pathlib import Path

# ==========================================================
# Project
# ==========================================================

PROJECT_NAME = "DataForge"

ROOT_DIRECTORY = Path(__file__).resolve().parent.parent

ENV_FILE = ROOT_DIRECTORY / ".env"

DEFAULT_TIMEZONE = "Africa/Johannesburg"

# ==========================================================
# Environment
# ==========================================================

DEFAULT_ENVIRONMENT = "development"

SUPPORTED_ENVIRONMENTS = (
    "development",
    "testing",
    "staging",
    "production",
)

# ==========================================================
# Storage
# ==========================================================

DEFAULT_STORAGE_BACKEND = "filesystem"

SUPPORTED_STORAGE_BACKENDS = (
    "filesystem",
    "minio",
    "s3",
    "azure",
    "gcs",
)

DEFAULT_STORAGE_BUCKET = "bronze"

# ==========================================================
# Logging
# ==========================================================

DEFAULT_LOG_LEVEL = "INFO"

DEFAULT_LOG_DIRECTORY = "logs"

SUPPORTED_LOG_LEVELS = (
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
)

# ==========================================================
# Database
# ==========================================================

DEFAULT_POSTGRES_PORT = 5432

# ==========================================================
# Redis
# ==========================================================

DEFAULT_REDIS_PORT = 6379

# ==========================================================
# MinIO
# ==========================================================

DEFAULT_MINIO_API_PORT = 9000

DEFAULT_MINIO_CONSOLE_PORT = 9001

DEFAULT_MINIO_SECURE = False

# ==========================================================
# Airflow
# ==========================================================

DEFAULT_AIRFLOW_PORT = 8080

DEFAULT_AIRFLOW_EXECUTOR = "LocalExecutor"

# ==========================================================
# Spark
# ==========================================================

DEFAULT_SPARK_MASTER_PORT = 7077

# ==========================================================
# Kafka
# ==========================================================

DEFAULT_KAFKA_PORT = 9092

# ==========================================================
# Monitoring
# ==========================================================

DEFAULT_PROMETHEUS_PORT = 9090

DEFAULT_GRAFANA_PORT = 3000

DEFAULT_MLFLOW_PORT = 5000

# ==========================================================
# API
# ==========================================================

DEFAULT_API_HOST = "0.0.0.0"

DEFAULT_API_PORT = 8000

# ==========================================================
# Miscellaneous
# ==========================================================

DEFAULT_ENCODING = "utf-8"

DEFAULT_FILE_CHUNK_SIZE = 1024 * 1024  # 1 MB

DEFAULT_REQUEST_TIMEOUT = 30
