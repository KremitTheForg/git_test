from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .database import Base, engine
from .routers import candidates as candidates_router
from .routers import auth as auth_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Candidate Intake API")

# Mount templates
templates = Jinja2Templates(directory="templates")

# Serve HTML form at "/"
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/candidate-form", response_class=HTMLResponse)
def candidate_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Include API routes
app.include_router(candidates_router.router)
app.include_router(auth_router.router)