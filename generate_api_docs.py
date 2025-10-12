#!/usr/bin/env python3
"""
Script to generate API documentation from OpenAPI spec.
"""

import sys
import os
import argparse

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from openapi.generator import OpenAPIDocGenerator
from openapi.version_manager import VersionManager
from license.validator import LicenseValidator
from license.config import Config


def main():
    parser = argparse.ArgumentParser(
        description="Generate beautiful API documentation from OpenAPI specs"
    )
    parser.add_argument(
        "spec", nargs="?", help="Path to OpenAPI spec file (omit if using --versions)"
    )
    parser.add_argument(
        "-o",
        "--output",
        default="api-docs",
        help="Output directory (default: api-docs)",
    )
    parser.add_argument(
        "-t",
        "--templates",
        default="templates/api",
        help="Templates directory (default: templates/api)",
    )
    parser.add_argument(
        "-s",
        "--static",
        default="static",
        help="Static assets directory (default: static)",
    )
    parser.add_argument("-l", "--license", help="License key for premium features")
    parser.add_argument(
        "--theme",
        choices=["default", "dark-pro", "light-pro", "modern"],
        help="Theme to use (requires PRO license for premium themes)",
    )
    parser.add_argument(
        "--versions",
        action="append",
        nargs=3,
        metavar=("VERSION", "SPEC_PATH", "LABEL"),
        help="Add API version: VERSION SPEC_PATH LABEL (PRO feature). Can be specified multiple times.",
    )
    parser.add_argument(
        "--default-version", help="Set default version to display (use with --versions)"
    )
    parser.add_argument(
        "--license-status", action="store_true", help="Show license status and exit"
    )
    parser.add_argument(
        "--init-config",
        action="store_true",
        help="Create sample configuration file and exit",
    )
    parser.add_argument(
        "--pdf",
        action="store_true",
        help="Export documentation to PDF (requires PRO license)",
    )

    args = parser.parse_args()

    if args.init_config:
        Config.create_sample_config()
        return

    if args.license_status:
        license_validator = LicenseValidator(args.license)
        license_validator.print_status()
        return

    print("ApiFlow - Beautiful API Documentation Generator")
    print(f"{'='*50}\n")
    print("Generating API documentation...")
    print(f"  Output: {args.output}")
    print(f"  Templates: {args.templates}")
    print(f"  Static: {args.static}")

    config = Config()

    if args.theme:
        config.set("theme", args.theme)

    version_manager = None
    if args.versions:
        print("\n📚 Setting up version management (PRO feature)...")
        version_manager = VersionManager()

        for version, spec_path, label in args.versions:
            is_default = (
                (args.default_version == version) if args.default_version else False
            )
            version_manager.add_version(version, spec_path, label, is_default)
            print(f"  ✓ Added version: {label} ({version}) from {spec_path}")

        if not args.default_version and version_manager.versions:
            # Set first as default if not specified
            first_version = list(version_manager.versions.keys())[0]
            version_manager.default_version = first_version
            print(f"  ℹ Default version set to: {first_version}")
    elif args.spec:
        print(f"  Spec: {args.spec}")
    else:
        if config.has_versions():
            print("\n📚 Loading versions from configuration...")
            version_manager = VersionManager()
            for v in config.get_versions():
                version_manager.add_version(
                    v["version"],
                    v["spec_path"],
                    v.get("label"),
                    v.get("is_default", False),
                )
                print(f"  ✓ Loaded version: {v.get('label', v['version'])}")
        else:
            args.spec = "example-api.yaml"
            print(f"  Spec: {args.spec}")

    generator = OpenAPIDocGenerator(
        spec_path=args.spec if not version_manager else None,
        output_dir=args.output,
        template_dir=args.templates,
        license_key=args.license,
        config=config,
        version_manager=version_manager,
    )

    generator.generate(static_dir=args.static, export_pdf=args.pdf)

    print(f"\n✓ Documentation generated successfully!")
    print(f"\nOpen {args.output}/index.html in your browser to view the docs.")

    license_info = generator.get_license_info()
    if not license_info["is_licensed"]:
        print(f"\n💡 Want premium features? Upgrade at:")
        print(f"   https://github.com/Ilia01/apiflow#pricing")


if __name__ == "__main__":
    main()
