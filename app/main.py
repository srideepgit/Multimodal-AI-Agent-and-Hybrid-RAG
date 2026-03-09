from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.router import router

app = FastAPI(

    title="Multimodal AI Agent",

    version="2.0.0",

)

# Allow the frontend (served from a different origin/port, e.g. a
# local file server or a separate dev server) to call this API.
# Tighten allow_origins to specific domains before deploying.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# Serve the static frontend (frontend/index.html, style.css, script.js)
# at the site root, e.g. http://localhost:8000/
_frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if _frontend_dir.exists():
    app.mount("/", StaticFiles(directory=_frontend_dir, html=True), name="frontend")