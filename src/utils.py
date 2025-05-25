"""
Utility functions for the TinyPEG project.
"""

import sys
import os

def setup_project_path():
    """
    Add the project root to the Python path.
    This function automatically detects the project root and adds it to sys.path.
    """
    # Get the directory containing this utils.py file (src/)
    src_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the project root (parent of src/)
    project_root = os.path.dirname(src_dir)
    
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    return project_root

def get_project_root():
    """
    Get the project root directory.
    """
    src_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(src_dir)
