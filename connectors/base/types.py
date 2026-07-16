"""
DataForge Connector Types

Shared data structures used by all connectors.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

# ==========================================================
# Connector Types
# ==========================================================

class ConnectorType(str, Enum):
    DATABASE = "database"
    FILE = "file"
    API = "api"
    STREAM = "stream"
    CLOUD = "cloud"
    ERP = "erp"
    CRM = "crm"
    DATA_WAREHOUSE = "data_warehouse"
    DATA_LAKE = "data_lake"
    CUSTOM = "custom"


# ==========================================================
# Connection Status
# ==========================================================

class ConnectionStatus(str, Enum):
    UNKNOWN = "unknown"
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    FAILED = "failed"
    AUTHENTICATION_FAILED = "authentication_failed"


# ==========================================================
# Pipeline Mode
# ==========================================================

class PipelineMode(str, Enum):
    BATCH = "batch"
    STREAMING = "streaming"
    HYBRID = "hybrid"


# ==========================================================
# Authentication
# ==========================================================

class AuthenticationType(str, Enum):
    NONE = "none"
    USERNAME_PASSWORD = "username_password"
    TOKEN = "token"
    API_KEY = "api_key"
    OAUTH2 = "oauth2"
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"


# ==========================================================
# Connector Configuration
# ==========================================================

@dataclass(slots=True)
class ConnectorConfig:
    """
    Generic configuration for every connector.
    """

    # Basic
    name: str
    connector_type: ConnectorType = ConnectorType.CUSTOM

    # Connection
    host: str | None = None
    port: int | None = None
    database: str | None = None

    # Credentials
    username: str | None = None
    password: str | None = None

    # Authentication
    auth_type: AuthenticationType = AuthenticationType.USERNAME_PASSWORD

    # SSL
    ssl_enabled: bool = False

    # Timeout
    timeout: int = 30

    # Extra connector-specific settings
    options: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Connector Metadata
# ==========================================================

@dataclass(slots=True)
class ConnectorMetadata:
    """
    Information describing a connector.
    """

    name: str
    version: str
    description: str
    author: str
    connector_type: ConnectorType

    supports_batch: bool = True
    supports_streaming: bool = False
    supports_incremental: bool = False

    tags: list[str] = field(default_factory=list)


# ==========================================================
# Connection Result
# ==========================================================

@dataclass(slots=True)
class ConnectionResult:
    """
    Result returned when testing a connection.
    """

    success: bool
    status: ConnectionStatus
    message: str

    timestamp: datetime = field(default_factory=datetime.utcnow)

    details: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Dataset Information
# ==========================================================

@dataclass(slots=True)
class DatasetInfo:
    """
    Metadata describing a dataset.
    """

    name: str

    schema: str | None = None

    rows: int | None = None

    columns: list[str] = field(default_factory=list)

    size_bytes: int | None = None


# ==========================================================
# Extraction Result
# ==========================================================

@dataclass(slots=True)
class ExtractionResult:
    """
    Result returned after data extraction.
    """

    success: bool

    records: int

    duration_seconds: float

    output_location: str

    metadata: dict[str, Any] = field(default_factory=dict)
