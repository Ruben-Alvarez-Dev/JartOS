#!/usr/bin/env python3
"""
Run the web dashboard server.

Usage:
    python scripts/run_web.py [--port 8000] [--host 0.0.0.0]
"""

import argparse
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


def main():
    parser = argparse.ArgumentParser(description="Run the web dashboard server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    args = parser.parse_args()

    import uvicorn
    from web.app import app

    print(f"\n{'='*50}")
    print("  Oposiciones Study System - Web Dashboard")
    print(f"{'='*50}")
    print(f"\n  Server running at: http://{args.host}:{args.port}")
    print(f"  Dashboard: http://localhost:{args.port}/dashboard")
    print(f"  API Docs: http://localhost:{args.port}/docs")
    print(f"\n  Press Ctrl+C to stop\n")

    uvicorn.run(
        "web.app:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
    )


if __name__ == "__main__":
    main()
