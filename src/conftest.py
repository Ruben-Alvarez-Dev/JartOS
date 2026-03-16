"""
Conftest for src directory

This prevents pytest from treating src/tests as a test directory.
"""

# This empty conftest.py in src/ ensures pytest doesn't try to
# collect tests from src/tests/ module during pytest discovery.
# The actual test configuration is in tests/conftest.py
