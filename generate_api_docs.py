#!/usr/bin/env python3
"""
Script to generate API documentation from OpenAPI spec.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from openapi.generator import OpenAPIDocGenerator


def main():
    # Paths
    spec_path = 'example-api.yaml'
    output_dir = 'api-docs'
    template_dir = 'templates/api'
    static_dir = 'static'

    print(f"Generating API documentation...")
    print(f"  Spec: {spec_path}")
    print(f"  Output: {output_dir}")
    print(f"  Templates: {template_dir}")
    print(f"  Static: {static_dir}")

    # Generate docs
    generator = OpenAPIDocGenerator(spec_path, output_dir, template_dir)
    generator.generate(static_dir=static_dir)

    print(f"\n✓ Documentation generated successfully!")
    print(f"\nOpen {output_dir}/index.html in your browser to view the docs.")


if __name__ == '__main__':
    main()
