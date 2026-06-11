"""File hashing and validation utilities."""

from __future__ import annotations

import hashlib
from pathlib import Path


def compute_sha256(filepath: Path, chunk_size: int = 8192) -> str:
    """Compute the SHA256 checksum of a file.

    Parameters
    ----------
    filepath : Path
        Path to the file to hash.
    chunk_size : int, optional
        Size of chunks to read into memory.

    Returns
    -------
    str
        The hex digest of the SHA256 hash.
    """
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(chunk_size), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def verify_checksum(filepath: Path, expected: str) -> bool:
    """Verify a file against an expected SHA256 checksum.

    Parameters
    ----------
    filepath : Path
        Path to the file.
    expected : str
        Expected SHA256 hex digest.

    Returns
    -------
    bool
        True if the checksum matches, False otherwise.
    """
    if not filepath.exists():
        return False
    return compute_sha256(filepath) == expected


def generate_file_manifest(
    directory: Path, ext_filter: str | None = None
) -> dict[str, str]:
    """Generate a manifest of SHA256 checksums for files in a directory.

    Distinct from :func:`cannaomics.utils.reproducibility.generate_manifest`,
    which records a full run manifest (parameters, package versions, etc.).

    Parameters
    ----------
    directory : Path
        Directory to scan.
    ext_filter : str, optional
        Only include files with this extension (e.g., ``".csv"``).

    Returns
    -------
    dict
        Mapping of relative file paths to their SHA256 checksums.
    """
    manifest: dict[str, str] = {}
    for path in directory.rglob("*"):
        if path.is_file():
            if ext_filter and path.suffix != ext_filter:
                continue
            rel_path = path.relative_to(directory).as_posix()
            manifest[rel_path] = compute_sha256(path)
    return manifest


# Backward-compatible alias (will be removed in a future version).
generate_manifest = generate_file_manifest

