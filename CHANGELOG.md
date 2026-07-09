# Changelog

All notable changes to this project will be documented in this file.

---

## v0.2.0 - Connector Framework

**Release Date:** July 9, 2026

### Added

- Enterprise Connector SDK
- BaseConnector abstraction
- ConnectorFactory
- ConnectorRegistry
- Standard connector configuration models
- Standard connector metadata models
- Standard exception hierarchy
- PostgreSQL connector implementation
- Dataset discovery
- SQL query execution
- Pandas DataFrame extraction
- Connection validation
- End-to-end PostgreSQL connector tests

### Infrastructure

- Dockerized PostgreSQL integration
- PostgreSQL host port changed from **5432** to **5433** to avoid conflicts with local PostgreSQL installations.

### Status

- ✅ Sprint 3 completed
- 🚀 Ready to begin Sprint 4 (Connector Registration & Discovery)
