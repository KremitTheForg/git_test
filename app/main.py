from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from app.database import Base, engine
from app.routers import candidates as candidates_router
from app.routers import auth as auth_router

# Create tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(title="Candidate Intake API")

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="super-secret-key")

# Templates
templates = Jinja2Templates(directory="templates")

# Root route: dashboard if logged in, otherwise login
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    user = request.session.get("user")
    if user:
        return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})
    else:
        return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/candidate-form", response_class=HTMLResponse)
def candidate_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Include routers
app.include_router(candidates_router.router)
app.include_router(auth_router.router)
