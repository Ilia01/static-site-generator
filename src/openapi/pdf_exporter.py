"""
PDF export functionality for API documentation.

PRO feature: Export generated HTML documentation to PDF format.
"""

from pathlib import Path
from typing import Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFExporter:
    """
    Exports HTML documentation to PDF format.

    Requires PRO or BUSINESS license.
    """

    def __init__(self, output_dir: Path):
        """
        Initialize PDF exporter.

        Args:
            output_dir: Directory containing generated HTML docs
        """
        self.output_dir = Path(output_dir)

    def export_to_pdf(self, output_filename: str = "api-documentation.pdf") -> Optional[Path]:
        """
        Export the main API documentation to PDF.

        Args:
            output_filename: Name of the PDF file to create

        Returns:
            Path to generated PDF file, or None if export failed
        """
        try:
            # Import weasyprint here so it's only required when using PDF export
            from weasyprint import HTML, CSS
        except ImportError:
            logger.error(
                "weasyprint not installed. Install it with: pip install weasyprint"
            )
            print("\n⚠️  PDF export requires weasyprint.")
            print("   Install it with: pip install weasyprint")
            print("   Note: weasyprint requires system dependencies (see docs)")
            return None

        index_html = self.output_dir / "index.html"
        if not index_html.exists():
            logger.error(f"Index HTML not found: {index_html}")
            return None

        pdf_output = self.output_dir / output_filename

        try:
            print(f"\n📄 Generating PDF: {output_filename}")
            print("   This may take a minute...")

            # Load HTML
            html = HTML(filename=str(index_html))

            # Custom CSS for PDF (optional improvements)
            pdf_css = CSS(string="""
                @page {
                    size: A4;
                    margin: 2cm;
                }

                body {
                    font-family: Arial, sans-serif;
                    font-size: 10pt;
                    line-height: 1.4;
                }

                /* Hide interactive elements in PDF */
                .theme-toggle,
                .search-box,
                #searchResults,
                .apiflow-footer,
                button,
                input {
                    display: none !important;
                }

                /* Better print layout */
                .sidebar {
                    page-break-after: always;
                }

                .endpoint-card {
                    page-break-inside: avoid;
                    margin-bottom: 1em;
                }

                code {
                    background: #f5f5f5;
                    padding: 2px 4px;
                    border-radius: 3px;
                }

                .code-block {
                    background: #f5f5f5;
                    padding: 10px;
                    border-radius: 5px;
                    page-break-inside: avoid;
                }
            """)

            # Generate PDF
            html.write_pdf(str(pdf_output), stylesheets=[pdf_css])

            print(f"✓ PDF exported successfully: {pdf_output}")
            return pdf_output

        except Exception as e:
            logger.error(f"PDF export failed: {e}")
            print(f"\n⚠️  PDF export failed: {e}")
            print("   Make sure weasyprint and its dependencies are installed.")
            return None

    def export_endpoint_to_pdf(self, endpoint_html: str, output_filename: str) -> Optional[Path]:
        """
        Export a single endpoint page to PDF.

        Args:
            endpoint_html: Filename of the endpoint HTML (e.g., 'get_pets.html')
            output_filename: Name of the PDF file to create

        Returns:
            Path to generated PDF file, or None if export failed
        """
        try:
            from weasyprint import HTML
        except ImportError:
            logger.error("weasyprint not installed")
            return None

        html_path = self.output_dir / endpoint_html
        if not html_path.exists():
            logger.error(f"HTML file not found: {html_path}")
            return None

        pdf_output = self.output_dir / output_filename

        try:
            html = HTML(filename=str(html_path))
            html.write_pdf(str(pdf_output))
            print(f"✓ Endpoint PDF exported: {pdf_output}")
            return pdf_output

        except Exception as e:
            logger.error(f"Endpoint PDF export failed: {e}")
            return None
