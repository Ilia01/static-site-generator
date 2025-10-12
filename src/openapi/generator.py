from pathlib import Path
from typing import Dict, Any, List, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape
from openapi.parser import OpenAPIParser
from openapi.version_manager import VersionManager
from openapi.pdf_exporter import PDFExporter
from license.validator import LicenseValidator
from license.features import FeatureManager, LicenseTier
from license.config import Config
import json
import shutil


class OpenAPIDocGenerator:
    """
    Generates HTML documentation from OpenAPI specification.
    """

    def __init__(self, spec_path: str = None, output_dir: str = None, template_dir: str = None,
                 license_key: Optional[str] = None, config: Optional[Config] = None,
                 version_manager: Optional[VersionManager] = None):
        """
        Initialize the documentation generator.

        Args:
            spec_path: Path to OpenAPI spec file (for single-spec mode)
            output_dir: Directory to output generated HTML files
            template_dir: Directory containing Jinja2 templates
            license_key: Optional license key for premium features
            config: Optional configuration object
            version_manager: Optional version manager for multi-version support
        """
        self.output_dir = Path(output_dir) if output_dir else Path('api-docs')
        self.template_dir = Path(template_dir) if template_dir else Path('templates/api')

        # Initialize configuration
        self.config = config or Config()

        # Get license key from parameter, config, or environment
        final_license_key = license_key or self.config.get_license_key()

        # Initialize license validator and feature manager
        self.license = LicenseValidator(final_license_key)
        self.features = FeatureManager(self.license.get_tier())

        # Initialize version manager
        self.version_manager = version_manager
        self.use_versioning = version_manager is not None and version_manager.has_multiple_versions()

        # For backward compatibility - single spec mode
        if spec_path and not version_manager:
            self.parser = OpenAPIParser(spec_path)
        else:
            self.parser = None

        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html", "xml"]),
        )

        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Print license status
        if not self.license.is_licensed():
            print("\n💡 Using FREE tier. Upgrade to PRO for premium features!")
            print("   Visit: https://github.com/Ilia01/apiflow#pricing\n")

        # Check version management feature
        if self.use_versioning and not self.features.has_feature('version_management'):
            print("\n⚠️  Version management requires PRO license. Using single version mode.")
            self.use_versioning = False

    def generate(self, static_dir: str = None, export_pdf: bool = False) -> None:
        """
        Generate all documentation pages.

        Args:
            static_dir: Optional path to static assets directory to copy
            export_pdf: Export documentation to PDF (requires PRO license)
        """
        # Copy static assets if provided
        if static_dir:
            self._copy_static_assets(static_dir)

        self._generate_index()
        self._generate_endpoint_pages()

        # PDF export (PRO feature)
        if export_pdf:
            if self.features.has_feature('pdf_export'):
                self._export_to_pdf()
            else:
                print("\n⚠️  PDF export requires PRO or BUSINESS license")
                print("   Upgrade at: https://gumroad.com/l/apiflow-pro")

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

        # Copy theme files if user has premium features
        if self.features.has_feature('premium_themes'):
            self._copy_theme_files(static_path)

        # Print versioning status
        if self.use_versioning:
            print(f"✓ Version management enabled ({len(self.version_manager.versions)} versions)")

    def _generate_index(self) -> None:
        """Generate the main index/overview page."""
        template = self.jinja_env.get_template("api_index.html")

        if self.use_versioning:
            # Multi-version mode
            default_version = self.version_manager.get_default_version()
            info = default_version.get_info()
            servers = default_version.get_servers()
            endpoints = default_version.get_endpoints()
            tags = default_version.get_tags()

            # Get all versions
            versions = self.version_manager.get_version_list()
            default_version_label = next((v['label'] for v in versions if v['is_default']), None)
        else:
            # Single spec mode
            info = self.parser.get_info()
            servers = self.parser.get_servers()
            endpoints = self.parser.get_endpoints()
            tags = self.parser.get_tags()
            versions = []
            default_version_label = None

        # Group endpoints by tag
        endpoints_by_tag = self._group_endpoints_by_tag(endpoints, tags)

        html = template.render(
            info=info,
            servers=servers,
            endpoints=endpoints,
            endpoints_by_tag=endpoints_by_tag,
            tags=tags,
            license_tier=self.license.get_tier().value,
            show_branding=self._should_show_branding(),
            selected_theme=self.get_selected_theme(),
            config=self.config,
            versions=versions if self.use_versioning else [],
            default_version_label=default_version_label,
            has_versioning=self.use_versioning,
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
                license_tier=self.license.get_tier().value,
                show_branding=self._should_show_branding(),
                selected_theme=self.get_selected_theme(),
                config=self.config,
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

    def _should_show_branding(self) -> bool:
        """
        Determine if ApiFlow branding should be shown.

        Branding can be removed with PRO license or higher.
        """
        # Check if user has remove_branding feature
        if self.features.has_feature('remove_branding'):
            # Check config setting
            return self.config.get('branding.show_apiflow_footer', False)

        # Free tier always shows branding
        return True

    def _copy_theme_files(self, static_path: Path) -> None:
        """
        Copy premium theme files to output directory.

        Only available with PRO or BUSINESS license.
        """
        themes_src = static_path / "themes"
        if not themes_src.exists():
            return

        themes_dest = self.output_dir / "themes"
        themes_dest.mkdir(exist_ok=True)

        # Copy all theme files
        for theme_file in themes_src.glob("*.css"):
            shutil.copy2(theme_file, themes_dest / theme_file.name)

        print(f"✓ Premium themes enabled ({len(list(themes_src.glob('*.css')))} themes available)")

    def get_selected_theme(self) -> Optional[str]:
        """
        Get the selected theme name.

        Returns:
            Theme name if premium theme is selected and available, None for default
        """
        if not self.features.has_feature('premium_themes'):
            return None

        theme = self.config.get('theme', 'default')
        if theme == 'default':
            return None

        # Validate theme exists
        available_themes = ['dark-pro', 'light-pro', 'modern']
        if theme in available_themes:
            return theme

        print(f"⚠️  Theme '{theme}' not found, using default")
        return None

    def get_license_info(self) -> Dict[str, Any]:
        """
        Get license information for display.

        Returns:
            Dictionary with license tier and features
        """
        return {
            'tier': self.license.get_tier().value,
            'is_licensed': self.license.is_licensed(),
            'features': self.features.get_available_features(),
        }

    def _export_to_pdf(self) -> None:
        """
        Export documentation to PDF (PRO feature).
        """
        try:
            exporter = PDFExporter(self.output_dir)
            pdf_path = exporter.export_to_pdf()

            if pdf_path:
                print(f"\n✓ PDF export complete: {pdf_path}")
                print(f"   API documentation exported to PDF format")
        except Exception as e:
            print(f"\n⚠️  PDF export failed: {e}")
            print("   Documentation HTML files were still generated successfully")
