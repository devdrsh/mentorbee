from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os
import asyncio

from app.routers import admin, batches, sessions, zoom, mentor_auth
from app.websockets import manager
from app.services.keep_alive import start_keep_alive

from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base

# Initialize DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MentorBee Class Link Management System",
    description="Centralized Zoom Meeting Link Management & WhatsApp Broadcast Dispatch for MentorBee Eduverse",
    version="1.0.0"
)

# Enable CORS for cloud and cross-origin compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static and templates dirs exist
os.makedirs("app/static/css", exist_ok=True)
os.makedirs("app/static/js", exist_ok=True)
os.makedirs("app/templates/admin", exist_ok=True)
os.makedirs("app/templates/mentor", exist_ok=True)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Health check endpoints for Cloud hosting (Render, Railway, Fly.io, AWS, Docker)
@app.get("/health")
@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "MentorBee Class Link Management System",
        "version": "1.0.0"
    }

@app.on_event("startup")
async def on_startup():
    # Start the keep-alive task to prevent Render inactivity sleep
    asyncio.create_task(start_keep_alive())

app.include_router(admin.router)
app.include_router(batches.router)
app.include_router(sessions.router)
app.include_router(zoom.router)
app.include_router(mentor_auth.router)

@app.websocket("/ws/mentor")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except (WebSocketDisconnect, Exception):
        manager.disconnect(websocket)


# Web Routes for Mentor
@app.get("/", response_class=HTMLResponse)
def get_mentor_dashboard(request: Request):
    return templates.TemplateResponse(request, "mentor/dashboard.html", {})

@app.get("/mentor/login", response_class=HTMLResponse)
def get_mentor_login(request: Request):
    return templates.TemplateResponse(request, "mentor/login.html", {})

# Web Routes for Admin
@app.get("/admin", response_class=HTMLResponse)
def get_admin_login(request: Request):
    return templates.TemplateResponse(request, "admin/login.html", {})

@app.get("/admin/dashboard", response_class=HTMLResponse)
def get_admin_dashboard(request: Request):
    return templates.TemplateResponse(request, "admin/dashboard.html", {})
