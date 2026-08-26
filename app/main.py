"""
SmartKYC FastAPI Application Entrypoint (MVC Architecture).
"""
import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.database import init_db
from app.controllers import api_router

# Initialize FastAPI App
app = FastAPI(
    title="SmartKYC Identity Verification API",
    description="Enterprise PAN & Aadhaar validation microservice built with clean MVC architecture.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Static & Template directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Register API Controllers (Router Layer)
app.include_router(api_router)


@app.on_event("startup")
def on_startup():
    """Initializes database tables and default administrator records."""
    init_db()


@app.get("/", response_class=HTMLResponse)
def serve_home_view(request: Request):
    """Serves the main MVC Glassmorphic View."""
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
