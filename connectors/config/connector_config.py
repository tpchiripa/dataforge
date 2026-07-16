"""
DataForge Connector Configuration

Defines the configuration shared by all DataForge connectors.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ConnectorConfig:
    """
    Configuration for a DataForge connector.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    name: str

    enabled: bool = True

    description: str = ""

    version: str = "1.0.0"

    # ---------------------------------------------------------
    # Connection
    # ---------------------------------------------------------

    host: str = "localhost"

    port: int = 0

    database: str = ""

    username: str = ""

    password: str = ""

    schema: str = ""

    connection_string: str = ""

    ssl: bool = False

    # ---------------------------------------------------------
    # Runtime
    # ---------------------------------------------------------

    timeout: int = 30

    retries: int = 3

    options: dict = field(default_factory=dict)

    # ---------------------------------------------------------

    def validate(self) -> None:
        """
        Validate connector configuration.
        """

        if not self.name.strip():
            raise ValueError(
                "Connector name cannot be empty."
            )

        if self.timeout < 0:
            raise ValueError(
                "Timeout cannot be negative."
            )

        if self.retries < 0:
            raise ValueError(
                "Retries cannot be negative."
            )

        if self.port < 0:
            raise ValueError(
                "Port cannot be negative."
            )

    # ---------------------------------------------------------

    def __post_init__(self):

        self.validate()

    # ---------------------------------------------------------

    @property
    def has_credentials(self) -> bool:
        """
        True if username/password are configured.
        """

        return bool(
            self.username and self.password
        )

    # ---------------------------------------------------------

    @property
    def address(self) -> str:
        """
        Host:Port representation.
        """

        if self.port:
            return f"{self.host}:{self.port}"

        return self.host

    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            "ConnectorConfig("
            f"name='{self.name}', "
            f"host='{self.host}', "
            f"port={self.port}, "
            f"database='{self.database}')"
        )
