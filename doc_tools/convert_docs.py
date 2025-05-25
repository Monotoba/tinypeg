#!/usr/bin/env python3
"""
Driver script for document conversion.

This script calls the appropriate conversion script based on command-line arguments.

Usage:
    python convert_docs.py md2html    # Convert Markdown to HTML
    python convert_docs.py html2pdf   # Convert HTML to PDF
    python convert_docs.py combine    # Combine PDFs into a single file
    python convert_docs.py all        # Run all conversions in sequence
"""

import os
import sys
import argparse
import importlib.util

def import_module_from_file(module_name, file_path):
    """Import a module from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Document conversion utility')
    parser.add_argument('conversion_type', choices=['md2html', 'html2pdf', 'combine', 'all'],
                        help='Type of conversion to perform')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Define paths to conversion scripts
    base_dir = os.path.dirname(os.path.abspath(__file__))
    utils_dir = os.path.join(base_dir, 'utils')
    
    md_to_html_script = os.path.join(utils_dir, 'convert_md_to_html.py')
    html_to_pdf_script = os.path.join(utils_dir, 'convert_html_to_pdf.py')
    combine_pdf_script = os.path.join(utils_dir, 'create_combined_pdf.py')
    
    # Check if scripts exist
    for script in [md_to_html_script, html_to_pdf_script, combine_pdf_script]:
        if not os.path.exists(script):
            print(f"Error: Script not found: {script}")
            return 1
    
    # Perform the requested conversion
    if args.conversion_type == 'md2html' or args.conversion_type == 'all':
        print("\n=== Converting Markdown to HTML ===")
        md_to_html_module = import_module_from_file('convert_md_to_html', md_to_html_script)
        md_to_html_module.convert_md_to_html()
    
    if args.conversion_type == 'html2pdf' or args.conversion_type == 'all':
        print("\n=== Converting HTML to PDF ===")
        html_to_pdf_module = import_module_from_file('convert_html_to_pdf', html_to_pdf_script)
        html_to_pdf_module.convert_html_to_pdf()
    
    if args.conversion_type == 'combine' or args.conversion_type == 'all':
        print("\n=== Combining PDFs ===")
        combine_pdf_module = import_module_from_file('create_combined_pdf', combine_pdf_script)
        combine_pdf_module.create_combined_pdf()
    
    print("\nConversion completed successfully!")
    
    # Print the locations of the generated files
    if args.conversion_type == 'md2html' or args.conversion_type == 'all':
        print(f"HTML files are located in: {os.path.join(base_dir, 'docs/ebook/html')}")
    
    if args.conversion_type == 'html2pdf' or args.conversion_type == 'all':
        print(f"PDF files are located in: {os.path.join(base_dir, 'docs/ebook/pdf')}")
    
    if args.conversion_type == 'combine' or args.conversion_type == 'all':
        combined_pdf = os.path.join(base_dir, 'docs/ebook/pdf', 'tinypeg_ebook.pdf')
        if os.path.exists(combined_pdf):
            print(f"Combined PDF is located at: {combined_pdf}")
        else:
            print(f"Warning: Combined PDF was not created at: {combined_pdf}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
