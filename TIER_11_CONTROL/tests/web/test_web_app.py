"""
Tests for Web Dashboard Application

These tests verify the web application works correctly.
Due to pytest's special handling of 'tests' directories, we use
a subprocess approach to test the app in isolation.
"""

import subprocess
import sys
import time
import httpx
import pytest
from pathlib import Path


class TestWebAppDirect:
    """Test web app by running it in a subprocess."""

    @pytest.fixture(scope="class")
    def server_process(self):
        """Start the web server in a subprocess."""
        import os
        env = os.environ.copy()
        env["PYTHONPATH"] = str(Path(__file__).parent.parent.parent.parent)
        
        # Start the server
        proc = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "web.app:app", "--host", "127.0.0.1", "--port", "8765"],
            cwd=str(Path(__file__).parent.parent.parent.parent / "TIER_04_INTERFACE"),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Wait for server to start
        time.sleep(2)

        yield proc

        # Cleanup
        proc.terminate()
        proc.wait(timeout=5)

    def test_server_starts(self, server_process):
        """Test that the server starts successfully."""
        assert server_process.poll() is None, "Server should be running"

    def test_dashboard_endpoint(self, server_process):
        """Test dashboard endpoint."""
        response = httpx.get("http://127.0.0.1:8765/dashboard")
        assert response.status_code == 200
        assert "Dashboard" in response.text

    def test_api_stats_endpoint(self, server_process):
        """Test API stats endpoint."""
        response = httpx.get("http://127.0.0.1:8765/api/dashboard/stats")
        assert response.status_code == 200
        data = response.json()
        assert "temario" in data
        assert "flashcards" in data
        assert "tests" in data

    def test_flashcards_page(self, server_process):
        """Test flashcards page."""
        response = httpx.get("http://127.0.0.1:8765/flashcards")
        assert response.status_code == 200

    def test_tests_page(self, server_process):
        """Test tests page."""
        response = httpx.get("http://127.0.0.1:8765/tests")
        assert response.status_code == 200

    def test_temario_page(self, server_process):
        """Test temario page."""
        response = httpx.get("http://127.0.0.1:8765/temario")
        assert response.status_code == 200

    def test_root_redirects(self, server_process):
        """Test root redirects to dashboard."""
        response = httpx.get("http://127.0.0.1:8765/", follow_redirects=False)
        assert response.status_code == 307
        assert "/dashboard" in response.headers.get("location", "")

    def test_static_files(self, server_process):
        """Test static file serving."""
        response = httpx.get("http://127.0.0.1:8765/static/css/style.css")
        assert response.status_code == 200

        response = httpx.get("http://127.0.0.1:8765/static/js/app.js")
        assert response.status_code == 200


class TestWebAppUnit:
    """Unit tests that don't require running the server."""

    def test_app_imports(self):
        """Test that the app can be imported."""
        import sys
        from pathlib import Path
        src_path = Path(__file__).parent.parent.parent.parent / "TIER_04_INTERFACE"
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        from web.app import app
        assert app is not None
        assert app.title == "Oposiciones Study System"

    def test_routes_registered(self):
        """Test that routes are registered."""
        import sys
        from pathlib import Path
        src_path = Path(__file__).parent.parent.parent.parent / "TIER_04_INTERFACE"
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        from web.app import app
        routes = [r.path for r in app.routes]
        assert "/dashboard" in routes
        assert "/flashcards" in routes
        assert "/tests" in routes
        assert "/temario" in routes

    def test_templates_exist(self):
        """Test that templates exist."""
        from pathlib import Path
        templates_dir = Path(__file__).parent.parent.parent.parent / "TIER_04_INTERFACE" / "web" / "templates"

        assert (templates_dir / "base.html").exists()
        assert (templates_dir / "dashboard.html").exists()
        assert (templates_dir / "flashcards.html").exists()
        assert (templates_dir / "tests.html").exists()
        assert (templates_dir / "temario.html").exists()

    def test_static_files_exist(self):
        """Test that static files exist."""
        from pathlib import Path
        static_dir = Path(__file__).parent.parent.parent.parent / "TIER_04_INTERFACE" / "web" / "static"

        assert (static_dir / "css" / "style.css").exists()
        assert (static_dir / "js" / "app.js").exists()
