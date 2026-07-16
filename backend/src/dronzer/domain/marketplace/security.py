import hashlib
from typing import Any

import structlog

logger = structlog.get_logger("dronzer.marketplace.security")


class SecurityScanner:
    """
    Validates the integrity and safety of uploaded Dronzer Packages.
    Checks digital signatures, hashes, and requested Sandbox Capabilities.
    """

    def __init__(self, sandbox_engine: Any = None):
        self.sandbox = sandbox_engine

        # High risk capabilities that require explicit IT Admin approval
        self.high_risk_capabilities = [
            "filesystem_write",
            "network_raw_sockets",
            "execute_shell",
            "read_env_vars",
        ]

    async def scan_package(self, package_path: str, manifest: dict[str, Any]) -> dict[str, Any]:
        """
        Runs a full security sweep on a `.dzpkg` file before it is allowed in the Registry.
        """
        logger.info(f"Initiating security scan for package: {manifest.get('name')}")

        # 1. Hash Validation
        file_hash = self._calculate_sha256(package_path)

        # 2. Digital Signature Verification (Mocked)
        # In production, uses GPG or Sigstore to verify the package was signed by the claimed Publisher
        is_signed = manifest.get("signature") is not None

        # 3. Capability Review
        requested_caps = manifest.get("capabilities", [])
        risk_level = "LOW"
        warnings = []

        for cap in requested_caps:
            if cap in self.high_risk_capabilities:
                risk_level = "HIGH"
                warnings.append(f"High risk capability requested: {cap}")

        # 4. Malware hooks (Placeholder for ClamAV / VirusTotal integrations)

        return {
            "status": "passed",
            "sha256": file_hash,
            "is_signed": is_signed,
            "risk_level": risk_level,
            "warnings": warnings,
        }

    def _calculate_sha256(self, file_path: str) -> str:
        """Calculates the SHA-256 hash of a file."""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except FileNotFoundError:
            return "hash_not_found"
