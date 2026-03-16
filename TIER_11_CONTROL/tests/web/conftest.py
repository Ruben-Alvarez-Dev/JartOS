"""
Conftest for web tests

Sets up the Python path correctly for tests.
IMPORTANT: This must run before any web module imports.
"""

import sys
from pathlib import Path

# Add src to path before any imports happen
src_path = Path(__file__).parent.parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))
