"""Hashing helpers."""
import hashlib


def sha256_str(text: str) -> str:
    """Return SHA-256 hex digest of input text."""
    return hashlib.sha256(text.encode()).hexdigest()
