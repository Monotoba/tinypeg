#!/usr/bin/env python3
"""
Test runner for TinyPEG.

This script runs all the tests in the tests directory and reports the results.
It also ensures that the tests are run with the correct Python path.
"""

import os
import sys
import unittest
import time

def run_tests():
    """Run all tests and report results."""
    start_time = time.time()
    
    # Ensure the src directory is in the Python path
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    print("=" * 70)
    print(f"Running TinyPEG tests from {project_root}")
    print("=" * 70)
    
    # Load all tests from the tests directory
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests')
    
    # Run the tests
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    
    # Print the summary
    print("\n" + "=" * 70)
    print(f"Test Summary:")
    print(f"  Tests run: {result.testsRun}")
    print(f"  Errors: {len(result.errors)}")
    print(f"  Failures: {len(result.failures)}")
    print(f"  Time elapsed: {elapsed_time:.2f} seconds")
    print("=" * 70)
    
    # Print any errors or failures
    if result.errors:
        print("\nErrors:")
        for test, error in result.errors:
            print(f"\n{test}:")
            print(error)
    
    if result.failures:
        print("\nFailures:")
        for test, failure in result.failures:
            print(f"\n{test}:")
            print(failure)
    
    # Exit with non-zero status if there were failures or errors
    return len(result.errors) + len(result.failures)

if __name__ == "__main__":
    sys.exit(run_tests())