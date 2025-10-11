from pathlib import Path
from typing import Dict, Any, List
from jinja2 import Environment, FileSystemLoader, select_autoescape
from openapi.parser import OpenAPIParser
import json
import shutil


class OpenAPIDocGenerator:
    """
    Generates HTML documentation from OpenAPI specification.
    """

    def __init__(self, spec_path: str, output_dir: str, template_dir: str):
        """
        Initialize the documentation generator.

        Args:
            spec_path: Path to OpenAPI spec file
            output_dir: Directory to output generated HTML files
            template_dir: Directory containing Jinja2 templates
        """
        self.parser = OpenAPIParser(spec_path)
        self.output_dir = Path(output_dir)
        self.template_dir = Path(template_dir)

        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html", "xml"]),
        )

        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, static_dir: str = None) -> None:
        """
        Generate all documentation pages.

        Args:
            static_dir: Optional path to static assets directory to copy
        """
        # Copy static assets if provided
        if static_dir:
            self._copy_static_assets(static_dir)

        self._generate_index()
        self._generate_endpoint_pages()

    def _copy_static_assets(self, static_dir: str) -> None:
        """Copy CSS, JS, and other static assets to output directory."""
        static_path = Path(static_dir)
        if not static_path.exists():
            return

        # Copy CSS files
        css_src = static_path / "css"
        if css_src.exists():
            css_dest = self.output_dir / "css"
            css_dest.mkdir(exist_ok=True)
            for css_file in css_src.glob("*.css"):
                shutil.copy2(css_file, css_dest / css_file.name)

        # Copy JS files
        js_src = static_path / "js"
        if js_src.exists():
            js_dest = self.output_dir / "js"
            js_dest.mkdir(exist_ok=True)
            for js_file in js_src.glob("*.js"):
                shutil.copy2(js_file, js_dest / js_file.name)

    def _generate_index(self) -> None:
        """Generate the main index/overview page."""
        template = self.jinja_env.get_template("api_index.html")

        info = self.parser.get_info()
        servers = self.parser.get_servers()
        endpoints = self.parser.get_endpoints()
        tags = self.parser.get_tags()

        # Group endpoints by tag
        endpoints_by_tag = self._group_endpoints_by_tag(endpoints, tags)

        html = template.render(
            info=info,
            servers=servers,
            endpoints=endpoints,
            endpoints_by_tag=endpoints_by_tag,
            tags=tags,
        )

        output_path = self.output_dir / "index.html"
        output_path.write_text(html, encoding="utf-8")

    def _generate_endpoint_pages(self) -> None:
        """Generate individual pages for each endpoint."""
        template = self.jinja_env.get_template("api_endpoint.html")

        endpoints = self.parser.get_endpoints()
        info = self.parser.get_info()

        for endpoint in endpoints:
            # Create a safe filename from method and path
            filename = self._endpoint_to_filename(endpoint)

            # Generate code examples
            code_examples = self._generate_code_examples(endpoint)

            html = template.render(
                endpoint=endpoint,
                info=info,
                code_examples=code_examples,
                endpoints=endpoints,  # For sidebar navigation
            )

            output_path = self.output_dir / filename
            output_path.write_text(html, encoding="utf-8")

    def _endpoint_to_filename(self, endpoint: Dict[str, Any]) -> str:
        """
        Convert endpoint to a safe filename.

        Example: GET /pets/{petId} -> get_pets_petid.html
        """
        method = endpoint["method"].lower()
        path = endpoint["path"]

        # Remove leading slash and replace special chars
        safe_path = path.lstrip("/").replace("/", "_").replace("{", "").replace("}", "")

        return f"{method}_{safe_path}.html"

    def _group_endpoints_by_tag(
        self, endpoints: List[Dict[str, Any]], tags: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Group endpoints by their tags."""
        grouped: Dict[str, List[Dict[str, Any]]] = {}

        # Initialize with defined tags
        for tag in tags:
            grouped[tag["name"]] = []

        # Add untagged group
        grouped["Untagged"] = []

        # Group endpoints
        for endpoint in endpoints:
            endpoint_tags = endpoint.get("tags", [])

            if not endpoint_tags:
                grouped["Untagged"].append(endpoint)
            else:
                for tag in endpoint_tags:
                    if tag not in grouped:
                        grouped[tag] = []
                    grouped[tag].append(endpoint)

        # Remove empty groups
        return {k: v for k, v in grouped.items() if v}

    def _generate_code_examples(self, endpoint: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate code examples for different languages.

        Returns:
            Dictionary mapping language to code example
        """
        examples = {}

        # Generate curl example
        examples["curl"] = self._generate_curl_example(endpoint)

        # Generate Python example
        examples["python"] = self._generate_python_example(endpoint)

        # Generate JavaScript example
        examples["javascript"] = self._generate_javascript_example(endpoint)

        return examples

    def _generate_curl_example(self, endpoint: Dict[str, Any]) -> str:
        """Generate curl command example."""
        method = endpoint["method"]
        path = endpoint["path"]
        servers = self.parser.get_servers()
        base_url = servers[0]["url"] if servers else "https://api.example.com"

        # Replace path parameters with example values
        example_path = path
        for param in endpoint["parameters"]:
            if param["in"] == "path":
                example_value = param.get("example", f"<{param['name']}>")
                example_path = example_path.replace(
                    f"{{{param['name']}}}", str(example_value)
                )

        curl = f"curl -X {method} \\\n  '{base_url}{example_path}'"

        # Add query parameters
        query_params = [p for p in endpoint["parameters"] if p["in"] == "query"]
        if query_params:
            curl += " \\\n  -G"
            for param in query_params:
                example_value = param.get("example", f"<{param['name']}>")
                curl += f" \\\n  --data-urlencode '{param['name']}={example_value}'"

        # Add request body if present
        if endpoint["request_body"]:
            curl += " \\\n  -H 'Content-Type: application/json' \\\n  -d '{}'"

        return curl

    def _generate_python_example(self, endpoint: Dict[str, Any]) -> str:
        """Generate Python requests example."""
        method = endpoint["method"].lower()
        path = endpoint["path"]
        servers = self.parser.get_servers()
        base_url = servers[0]["url"] if servers else "https://api.example.com"

        # Replace path parameters
        example_path = path
        for param in endpoint["parameters"]:
            if param["in"] == "path":
                example_value = param.get("example", f"<{param['name']}>")
                example_path = example_path.replace(
                    f"{{{param['name']}}}", str(example_value)
                )

        code = f"import requests\n\n"
        code += f"url = '{base_url}{example_path}'\n"

        # Add query parameters
        query_params = [p for p in endpoint["parameters"] if p["in"] == "query"]
        if query_params:
            code += "params = {\n"
            for param in query_params:
                example_value = param.get("example", f"<{param['name']}>")
                code += f"    '{param['name']}': '{example_value}',\n"
            code += "}\n\n"
            code += f"response = requests.{method}(url, params=params)\n"
        else:
            code += f"\nresponse = requests.{method}(url)\n"

        code += "print(response.json())"

        return code

    def _generate_javascript_example(self, endpoint: Dict[str, Any]) -> str:
        """Generate JavaScript fetch example."""
        method = endpoint["method"]
        path = endpoint["path"]
        servers = self.parser.get_servers()
        base_url = servers[0]["url"] if servers else "https://api.example.com"

        # Replace path parameters
        example_path = path
        for param in endpoint["parameters"]:
            if param["in"] == "path":
                example_value = param.get("example", f"<{param['name']}>")
                example_path = example_path.replace(
                    f"{{{param['name']}}}", str(example_value)
                )

        code = f"const url = '{base_url}{example_path}';\n\n"
        code += f"fetch(url, {{\n"
        code += f"  method: '{method}',\n"

        if endpoint["request_body"]:
            code += "  headers: {\n"
            code += "    'Content-Type': 'application/json',\n"
            code += "  },\n"
            code += "  body: JSON.stringify({}),\n"

        code += "})\n"
        code += "  .then(response => response.json())\n"
        code += "  .then(data => console.log(data));"

        return code
