#!/usr/bin/env python3
"""
Script to convert HTML files to PDF.
Converts all .html files from docs/ebook/html to PDF and saves them in docs/ebook/pdf.
"""

import os
import sys
import glob
from weasyprint import HTML

def convert_html_to_pdf():
    # Get the current working directory
    current_dir = os.getcwd()
    print(f"Current working directory: {current_dir}")

    # Define directories relative to project root
    # Go up three levels: utils -> doc_tools -> project_root
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    html_dir = os.path.join(base_dir, 'docs/ebook/html')
    pdf_dir = os.path.join(base_dir, 'docs/ebook/pdf')

    print(f"HTML directory: {html_dir}")
    print(f"PDF directory: {pdf_dir}")

    # Check if HTML directory exists
    if not os.path.exists(html_dir):
        print(f"Error: HTML directory does not exist: {html_dir}")
        return

    # Ensure PDF directory exists
    os.makedirs(pdf_dir, exist_ok=True)

    # Get all HTML files
    html_files = glob.glob(os.path.join(html_dir, '*.html'))
    print(f"Found {len(html_files)} HTML files")

    # Convert each HTML file to PDF
    for html_file in html_files:
        try:
            # Get the filename without extension
            base_name = os.path.basename(html_file)
            file_name_without_ext = os.path.splitext(base_name)[0]
            pdf_file = os.path.join(pdf_dir, file_name_without_ext + '.pdf')

            print(f"Processing {html_file} -> {pdf_file}")

            # Convert HTML to PDF
            HTML(filename=html_file).write_pdf(pdf_file)

            print(f"Successfully converted {html_file} to {pdf_file}")
        except Exception as e:
            print(f"Error processing {html_file}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    try:
        convert_html_to_pdf()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
