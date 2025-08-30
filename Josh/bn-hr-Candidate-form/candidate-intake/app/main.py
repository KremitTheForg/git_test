from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .database import Base, engine
from .routers import candidates as candidates_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Candidate Intake API")

# Mount templates
templates = Jinja2Templates(directory="templates")

# Serve HTML form at "/"
@app.get("/", response_class=HTMLResponse)
def serve_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Include API routes
app.include_router(candidates_router.router)
