from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from .. import schemas, crud, database, models

router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="templates")


# ✅ New GET route for showing the login form
@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(database.get_db)
):
    db_user = crud.get_user_by_email(db, email=email)
    if not db_user or not crud.verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Save session
    request.session["user"] = {
        "id": db_user.id,
        "username": db_user.username,
        "email": db_user.email,
    }

    print("Session saved:", request.session)

    candidate = db.query(models.Candidate).filter(models.Candidate.user_id == db_user.id).first()
    if not candidate:
        # fallback by email for legacy rows
        candidate = db.query(models.Candidate).filter(models.Candidate.email == db_user.email).first()

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": db_user, "candidate": candidate}
    )


@router.get("/logout")
@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)
