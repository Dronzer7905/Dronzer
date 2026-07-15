import json
import re
import zipfile
from typing import Any

import structlog

logger = structlog.get_logger("dronzer.marketplace.engine")

class SemanticVersion:
    """Utility for comparing Semantic Versions (e.g. 1.2.0 > 1.1.9)"""

    @staticmethod
    def parse(version_string: str) -> tuple[int, int, int]:
        match = re.match(r"^(\d+)\.(\d+)\.(\d+)", version_string)
        if not match:
            raise ValueError(f"Invalid Semantic Version format: {version_string}")
        return int(match.group(1)), int(match.group(2)), int(match.group(3))

    @staticmethod
    def is_compatible(required: str, available: str) -> bool:
        """
        Naive check: '>=1.0.0'. In production, this would use a full SemVer parser library.
        """
        # Simplification for placeholder
        if required.startswith(">="):
            req_ver = required[2:]
            return SemanticVersion.parse(available) >= SemanticVersion.parse(req_ver)
        return available == required

class PackageEngine:
    """
    Core engine responsible for parsing `.dzpkg` archives (which are just ZIPs),
    extracting the `manifest.json`, and validating the package structure before 
    it gets installed into the Dronzer ecosystem.
    """

    async def extract_manifest(self, package_path: str) -> dict[str, Any]:
        """
        Reads a .dzpkg archive and extracts the manifest.json file.
        """
        logger.debug(f"Extracting manifest from {package_path}")

        try:
            with zipfile.ZipFile(package_path, 'r') as zip_ref:
                if 'manifest.json' not in zip_ref.namelist():
                    raise ValueError("Invalid .dzpkg: Missing manifest.json")

                with zip_ref.open('manifest.json') as f:
                    manifest = json.loads(f.read().decode('utf-8'))

            self._validate_manifest(manifest)
            return manifest

        except Exception as e:
            logger.error("Failed to parse package archive", error=str(e))
            raise e

    def _validate_manifest(self, manifest: dict[str, Any]):
        """
        Ensures the manifest conforms to the Dronzer Package Schema.
        """
        required_fields = ["name", "version", "publisher", "type"]
        for field in required_fields:
            if field not in manifest:
                raise ValueError(f"Manifest missing required field: {field}")

        # Validate SemVer format
        SemanticVersion.parse(manifest["version"])
