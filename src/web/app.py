"""
FastAPI Web Application for Oposiciones Study System

Main application entry point with route configuration.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

# Route modules
from .routes import dashboard, flashcards, tests, temario

# Create FastAPI app
app = FastAPI(
    title="Oposiciones Study System",
    description="Web dashboard for study management",
    version="0.1.0",
)

# Paths
BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Include routers
app.include_router(dashboard.router, tags=["Dashboard"])
app.include_router(flashcards.router, tags=["Flashcards"])
app.include_router(tests.router, tags=["Tests"])
app.include_router(temario.router, tags=["Temario"])


@app.get("/")
async def root():
    """Redirect root to dashboard."""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/dashboard")


# Make templates available to routes
app.state.templates = templates
