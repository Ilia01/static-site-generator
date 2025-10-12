"""Configuration management for ApiFlow."""

import os
from pathlib import Path
from typing import Optional, Dict, Any, List
import json


class Config:
    """
    Manages configuration for ApiFlow documentation generator.

    Configuration can be loaded from:
    1. Environment variables
    2. Config file (apiflow.json)
    3. Command-line arguments
    """

    CONFIG_FILE = "apiflow.json"

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration.

        Args:
            config_path: Optional path to config file
        """
        self.config_path = Path(config_path) if config_path else Path(self.CONFIG_FILE)
        self.config: Dict[str, Any] = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file if it exists."""
        default_config = {
            'license_key': None,
            'theme': 'default',
            'branding': {
                'show_apiflow_footer': True,
                'custom_footer': None,
                'logo_url': None,
            },
            'features': {
                'search': True,
                'dark_mode': True,
                'code_examples': True,
            },
            'versions': []  # List of API versions
        }

        if not self.config_path.exists():
            return default_config

        try:
            with open(self.config_path, 'r') as f:
                user_config = json.load(f)
                # Merge with defaults
                default_config.update(user_config)
                return default_config
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️  Error loading config file: {e}")
            return default_config

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.

        Args:
            key: Configuration key (supports dot notation, e.g., 'branding.logo_url')
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default

            if value is None:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value.

        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self.config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def save(self) -> None:
        """Save configuration to file."""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            print(f"✓ Configuration saved to {self.config_path}")
        except IOError as e:
            print(f"⚠️  Error saving config file: {e}")

    def get_license_key(self) -> Optional[str]:
        """
        Get license key from config or environment variable.

        Returns:
            License key if found, None otherwise
        """
        # Check environment variable first
        env_key = os.environ.get('APIFLOW_LICENSE_KEY')
        if env_key:
            return env_key

        # Then check config file
        return self.get('license_key')

    @staticmethod
    def create_sample_config(path: str = "apiflow.json") -> None:
        """
        Create a sample configuration file.

        Args:
            path: Path where to create the config file
        """
        sample_config = {
            "license_key": "APIFLOW-PRO-xxxxxxxxxxxxxxxx",
            "theme": "default",
            "_theme_options": "default | dark-pro | light-pro | modern (PRO license required for premium themes)",
            "branding": {
                "show_apiflow_footer": True,
                "custom_footer": "© 2024 Your Company",
                "logo_url": None
            },
            "features": {
                "search": True,
                "dark_mode": True,
                "code_examples": True
            },
            "versions": [
                {
                    "_comment": "Version management (PRO feature) - document multiple API versions",
                    "version": "v1",
                    "spec_path": "specs/api-v1.yaml",
                    "label": "Version 1.0 (Legacy)",
                    "is_default": False
                },
                {
                    "version": "v2",
                    "spec_path": "specs/api-v2.yaml",
                    "label": "Version 2.0 (Current)",
                    "is_default": True
                }
            ]
        }

        config_path = Path(path)
        with open(config_path, 'w') as f:
            json.dump(sample_config, f, indent=2)

        print(f"✓ Sample configuration created at {config_path}")
        print("  Edit this file and add your license key to unlock premium features.")
        print("\n  Available themes (PRO license required):")
        print("    • dark-pro  - Modern dark theme with purple accents")
        print("    • light-pro - Clean professional light theme")
        print("    • modern    - Contemporary design with vibrant gradients")
        print("\n  Version management (PRO license required):")
        print("    Configure multiple API versions in the 'versions' array")
        print("    See VERSIONING.md for detailed documentation")

    def get_versions(self) -> List[Dict[str, Any]]:
        """
        Get configured API versions.

        Returns:
            List of version configurations
        """
        return self.get('versions', [])

    def add_version(self, version: str, spec_path: str, label: Optional[str] = None,
                   is_default: bool = False) -> None:
        """
        Add an API version to configuration.

        Args:
            version: Version identifier (e.g., "v1", "1.0.0")
            spec_path: Path to OpenAPI spec file
            label: Optional display label
            is_default: Whether this is the default version
        """
        versions = self.get_versions()

        # Remove existing version with same identifier
        versions = [v for v in versions if v.get('version') != version]

        # Add new version
        versions.append({
            'version': version,
            'spec_path': spec_path,
            'label': label or version,
            'is_default': is_default
        })

        self.set('versions', versions)

    def has_versions(self) -> bool:
        """Check if any versions are configured."""
        return len(self.get_versions()) > 0
