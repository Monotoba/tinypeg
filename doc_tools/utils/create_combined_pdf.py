#!/usr/bin/env python3
"""
Script to create a combined PDF from all the individual chapter PDFs.
"""

import os
import sys
from PyPDF2 import PdfMerger

def create_combined_pdf():
    # Define directories relative to project root
    # Go up three levels: utils -> doc_tools -> project_root
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    pdf_dir = os.path.join(base_dir, 'docs/ebook/pdf')
    output_file = os.path.join(pdf_dir, 'tinypeg_ebook.pdf')

    # Check if PDF directory exists
    if not os.path.exists(pdf_dir):
        print(f"Error: PDF directory does not exist: {pdf_dir}")
        return

    # Define the order of chapters
    chapter_order = [
        'index.pdf',
        'preface.pdf',
        'contents.pdf',
        'chapter01_peg_basics.pdf',
        'chapter02_library_overview.pdf',
        'chapter03_building_parsers.pdf',
        'chapter04_examples.pdf',
        'chapter05_tiny_language.pdf',
        'appendix_a_peg_reference.pdf',
        'appendix_b_testing.pdf',
        'appendix_c_tinycl_reference.pdf'
    ]

    # Create a PDF merger object
    merger = PdfMerger()

    # Add each PDF to the merger
    for chapter in chapter_order:
        chapter_path = os.path.join(pdf_dir, chapter)
        if os.path.exists(chapter_path):
            print(f"Adding {chapter} to the combined PDF")
            try:
                merger.append(chapter_path)
            except Exception as e:
                print(f"Error adding {chapter}: {e}")
        else:
            print(f"Warning: {chapter} not found")

    # Write the combined PDF to disk
    print(f"Writing combined PDF to {output_file}")
    merger.write(output_file)
    merger.close()

    print(f"Successfully created combined PDF: {output_file}")

if __name__ == "__main__":
    try:
        create_combined_pdf()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
