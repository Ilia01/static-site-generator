import yaml
import json
from pathlib import Path
from typing import Dict, List, Any, Optional


class OpenAPIParser:
    """
    Parses OpenAPI 3.0 specification files (YAML or JSON)
    and extracts structured data for documentation generation.
    """

    def __init__(self, spec_path: str):
        """
        Initialize parser with path to OpenAPI spec file.

        Args:
            spec_path: Path to OpenAPI YAML or JSON file
        """
        self.spec_path = Path(spec_path)
        self.spec: Dict[str, Any] = {}
        self._load_spec()

    def _load_spec(self) -> None:
        """Load and parse the OpenAPI specification file."""
        if not self.spec_path.exists():
            raise FileNotFoundError(f"OpenAPI spec not found: {self.spec_path}")

        with open(self.spec_path, "r", encoding="utf-8") as f:
            if self.spec_path.suffix in [".yaml", ".yml"]:
                self.spec = yaml.safe_load(f)
            elif self.spec_path.suffix == ".json":
                self.spec = json.load(f)
            else:
                raise ValueError(f"Unsupported file format: {self.spec_path.suffix}")

        # Basic validation
        if "openapi" not in self.spec:
            raise ValueError("Invalid OpenAPI spec: missing 'openapi' field")

        if not self.spec["openapi"].startswith("3."):
            raise ValueError(f"Only OpenAPI 3.x is supported, got: {self.spec['openapi']}")

    def get_info(self) -> Dict[str, Any]:
        """
        Get API metadata (title, version, description, etc.)

        Returns:
            Dictionary with API info
        """
        return self.spec.get("info", {})

    def get_servers(self) -> List[Dict[str, Any]]:
        """
        Get list of server URLs.

        Returns:
            List of server objects
        """
        return self.spec.get("servers", [])

    def get_paths(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all API paths/endpoints.

        Returns:
            Dictionary mapping path to operations
        """
        return self.spec.get("paths", {})

    def get_endpoints(self) -> List[Dict[str, Any]]:
        """
        Get all endpoints as a flat list with parsed details.

        Returns:
            List of endpoint objects with method, path, summary, etc.
        """
        endpoints = []
        paths = self.get_paths()

        for path, path_item in paths.items():
            # Common parameters for all operations in this path
            common_params = path_item.get("parameters", [])

            for method in ["get", "post", "put", "patch", "delete", "options", "head"]:
                if method not in path_item:
                    continue

                operation = path_item[method]

                # Merge common and operation-specific parameters
                params = common_params + operation.get("parameters", [])

                endpoint = {
                    "path": path,
                    "method": method.upper(),
                    "operation_id": operation.get("operationId", f"{method}_{path}"),
                    "summary": operation.get("summary", ""),
                    "description": operation.get("description", ""),
                    "parameters": self._parse_parameters(params),
                    "request_body": self._parse_request_body(operation.get("requestBody")),
                    "responses": self._parse_responses(operation.get("responses", {})),
                    "tags": operation.get("tags", []),
                    "deprecated": operation.get("deprecated", False),
                }

                endpoints.append(endpoint)

        return endpoints

    def _parse_parameters(self, params: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Parse parameter objects into simplified format."""
        parsed = []
        for param in params:
            parsed.append({
                "name": param.get("name", ""),
                "in": param.get("in", ""),  # query, path, header, cookie
                "description": param.get("description", ""),
                "required": param.get("required", False),
                "schema": param.get("schema", {}),
                "example": param.get("example"),
            })
        return parsed

    def _parse_request_body(self, request_body: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Parse request body object."""
        if not request_body:
            return None

        content = request_body.get("content", {})

        return {
            "description": request_body.get("description", ""),
            "required": request_body.get("required", False),
            "content": content,
        }

    def _parse_responses(self, responses: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse response objects."""
        parsed = []
        for status_code, response in responses.items():
            parsed.append({
                "status_code": status_code,
                "description": response.get("description", ""),
                "content": response.get("content", {}),
            })
        return parsed

    def get_tags(self) -> List[Dict[str, Any]]:
        """
        Get all tags for grouping endpoints.

        Returns:
            List of tag objects with name and description
        """
        return self.spec.get("tags", [])

    def get_components(self) -> Dict[str, Any]:
        """
        Get reusable components (schemas, responses, parameters, etc.)

        Returns:
            Components object
        """
        return self.spec.get("components", {})

    def get_schemas(self) -> Dict[str, Any]:
        """
        Get all schema definitions.

        Returns:
            Dictionary of schema objects
        """
        components = self.get_components()
        return components.get("schemas", {})
