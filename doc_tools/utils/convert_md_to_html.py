#!/usr/bin/env python3
"""
Script to convert Markdown files to HTML.
Converts all .md files from docs/ebook/markdown to HTML and saves them in docs/ebook/html.
"""

import os
import sys
import markdown
import glob

def convert_md_to_html():
    # Get the current working directory
    current_dir = os.getcwd()
    print(f"Current working directory: {current_dir}")

    # Define directories relative to project root
    # Go up three levels: utils -> doc_tools -> project_root
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    markdown_dir = os.path.join(base_dir, 'docs/ebook/markdown')
    html_dir = os.path.join(base_dir, 'docs/ebook/html')

    print(f"Markdown directory: {markdown_dir}")
    print(f"HTML directory: {html_dir}")

    # Check if markdown directory exists
    if not os.path.exists(markdown_dir):
        print(f"Error: Markdown directory does not exist: {markdown_dir}")
        return

    # Ensure HTML directory exists
    os.makedirs(html_dir, exist_ok=True)

    # Get all markdown files
    md_files = glob.glob(os.path.join(markdown_dir, '*.md'))
    print(f"Found {len(md_files)} markdown files")

    # Basic HTML template
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
pre {{ background-color: #f5f5f5; padding: 10px; border-radius: 5px; overflow-x: auto; }}
code {{ font-family: monospace; }}
h1, h2, h3 {{ color: #333; }}
a {{ color: #0066cc; }}
    </style>
</head>
<body>
{content}
</body>
</html>
"""

    # Convert each markdown file to HTML
    for md_file in md_files:
        try:
            # Get the filename without extension
            base_name = os.path.basename(md_file)
            file_name_without_ext = os.path.splitext(base_name)[0]
            html_file = os.path.join(html_dir, file_name_without_ext + '.html')

            print(f"Processing {md_file} -> {html_file}")

            # Read markdown content
            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()

            # Convert to HTML (basic conversion without extensions)
            html_content = markdown.markdown(md_content)

            # Get title from the first heading or use filename
            title = file_name_without_ext.replace('_', ' ').title()
            if md_content.startswith('# '):
                title = md_content.split('\n')[0].lstrip('# ')

            # Insert into template
            full_html = html_template.format(title=title, content=html_content)

            # Write HTML file
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(full_html)

            print(f"Successfully converted {md_file} to {html_file}")
        except Exception as e:
            print(f"Error processing {md_file}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    try:
        convert_md_to_html()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
