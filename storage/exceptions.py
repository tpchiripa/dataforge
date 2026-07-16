"""
Storage Exceptions
"""


class StorageError(Exception):
    """Base storage exception."""


class StorageConnectionError(StorageError):
    """Raised when storage cannot be reached."""


class BucketNotFoundError(StorageError):
    """Bucket does not exist."""


class ObjectNotFoundError(StorageError):
    """Object does not exist."""


class UploadError(StorageError):
    """Upload failed."""


class DownloadError(StorageError):
    """Download failed."""


class DeleteError(StorageError):
    """Delete failed."""
