#!/usr/bin/env python3
"""
Setup script for TinyPEG - A Complete PEG Parser Library with TinyCL Programming Language
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read the requirements
def read_requirements():
    requirements = []
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#"):
                    requirements.append(line)
    return requirements

setup(
    name="tinypeg",
    version="1.0.0",
    author="Randall Morgan",
    author_email="randall.morgan@example.com",  # Update with actual email if desired
    description="A complete PEG parser library with TinyCL programming language implementation",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Monotoba/tinypeg",  # Update with actual GitHub URL when available
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Compilers",
        "Topic :: Software Development :: Interpreters",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: General",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=21.0.0",
            "flake8>=3.8.0",
        ],
    },

    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.tcl"],
    },
    project_urls={
        "Bug Reports": "https://github.com/Monotoba/tinypeg/issues",
        "Source": "https://github.com/Monotoba/tinypeg",
        "Documentation": "https://github.com/Monotoba/tinypeg/blob/main/README.md",
        "E-book": "https://github.com/Monotoba/tinypeg/blob/main/docs/ebook/pdf/tinypeg_complete_ebook.pdf",
    },
    keywords="parser peg parsing-expression-grammar compiler interpreter language",
    zip_safe=False,
)
