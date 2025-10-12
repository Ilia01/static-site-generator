"""
API Version Management for ApiFlow.

Handles multiple versions of API specifications and generates
unified documentation with version switching capabilities.
"""

from typing import Dict, List, Any, Optional
from openapi.parser import OpenAPIParser


class VersionedAPI:
    """Represents a single version of an API."""

    def __init__(self, version: str, spec_path: str, label: Optional[str] = None):
        """
        Initialize a versioned API.

        Args:
            version: Version identifier (e.g., "1.0.0", "v1", "2.0")
            spec_path: Path to the OpenAPI specification file
            label: Optional display label (defaults to version)
        """
        self.version = version
        self.spec_path = spec_path
        self.label = label or version
        self.parser = OpenAPIParser(spec_path)

    def get_info(self) -> Dict[str, Any]:
        """Get API info with version metadata."""
        info = self.parser.get_info()
        info["api_version"] = self.version
        info["version_label"] = self.label
        return info

    def get_endpoints(self) -> List[Dict[str, Any]]:
        """Get endpoints with version metadata."""
        endpoints = self.parser.get_endpoints()
        for endpoint in endpoints:
            endpoint["api_version"] = self.version
        return endpoints

    def get_servers(self) -> List[Dict[str, Any]]:
        """Get servers from this version."""
        return self.parser.get_servers()

    def get_tags(self) -> List[Dict[str, Any]]:
        """Get tags from this version."""
        return self.parser.get_tags()


class VersionManager:
    """Manages multiple API versions and generates unified documentation."""

    def __init__(self):
        """Initialize the version manager."""
        self.versions: Dict[str, VersionedAPI] = {}
        self.default_version: Optional[str] = None

    def add_version(
        self,
        version: str,
        spec_path: str,
        label: Optional[str] = None,
        is_default: bool = False,
    ) -> None:
        """
        Add an API version.

        Args:
            version: Version identifier (e.g., "v1", "v2")
            spec_path: Path to OpenAPI spec file
            label: Optional display label
            is_default: Whether this is the default version to show
        """
        versioned_api = VersionedAPI(version, spec_path, label)
        self.versions[version] = versioned_api

        if not self.default_version or is_default:
            self.default_version = version

    def get_version(self, version: str) -> Optional[VersionedAPI]:
        """Get a specific API version."""
        return self.versions.get(version)

    def get_default_version(self) -> Optional[VersionedAPI]:
        """Get the default API version."""
        if self.default_version:
            return self.versions.get(self.default_version)
        return None

    def get_all_versions(self) -> List[VersionedAPI]:
        """Get all API versions sorted by version string."""
        return [self.versions[v] for v in sorted(self.versions.keys(), reverse=True)]

    def get_version_list(self) -> List[Dict[str, str]]:
        """
        Get a list of all versions for the UI selector.

        Returns:
            List of dicts with 'version' and 'label' keys
        """
        return [
            {
                "version": v.version,
                "label": v.label,
                "is_default": v.version == self.default_version,
            }
            for v in self.get_all_versions()
        ]

    def has_multiple_versions(self) -> bool:
        """Check if multiple versions are available."""
        return len(self.versions) > 1

    def get_combined_endpoints(self) -> List[Dict[str, Any]]:
        """
        Get all endpoints from all versions combined.

        Returns endpoints grouped by version, with the default version first.
        """
        all_endpoints = []

        if self.default_version:
            default = self.get_default_version()
            if default:
                all_endpoints.extend(default.get_endpoints())

        for version in sorted(self.versions.keys(), reverse=True):
            if version != self.default_version:
                all_endpoints.extend(self.versions[version].get_endpoints())

        return all_endpoints

    def get_endpoints_by_version(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get endpoints grouped by version.

        Returns:
            Dict mapping version to list of endpoints
        """
        return {version: api.get_endpoints() for version, api in self.versions.items()}

    def get_version_comparison(self) -> Dict[str, Any]:
        """
        Generate comparison data between versions.

        Useful for showing what changed between versions.
        """
        if not self.has_multiple_versions():
            return {}

        comparison = {
            "versions": list(self.versions.keys()),
            "endpoint_counts": {},
            "new_endpoints": {},
            "removed_endpoints": {},
        }

        versions_sorted = sorted(self.versions.keys())

        for i, version in enumerate(versions_sorted):
            api = self.versions[version]
            endpoints = api.get_endpoints()
            comparison["endpoint_counts"][version] = len(endpoints)

            if i > 0:
                prev_version = versions_sorted[i - 1]
                prev_api = self.versions[prev_version]
                prev_endpoints = {
                    f"{e['method']} {e['path']}" for e in prev_api.get_endpoints()
                }
                curr_endpoints = {f"{e['method']} {e['path']}" for e in endpoints}

                comparison["new_endpoints"][version] = list(
                    curr_endpoints - prev_endpoints
                )
                comparison["removed_endpoints"][version] = list(
                    prev_endpoints - curr_endpoints
                )

        return comparison
