from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from .. import schemas, crud, database, models

router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="templates")

@router.post("/register", response_model=schemas.UserOut)
def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(database.get_db)
):
    db_user = crud.get_user_by_email(db, email=email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_data = schemas.UserCreate(username=username, email=email, password=password)
    return crud.create_user(db=db, user=user_data)

##

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

    # Try to fetch candidate profile linked by email
    candidate = db.query(models.Candidate).filter(models.Candidate.email == email).first()

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": db_user, "candidate": candidate}
    )

@router.post("/logout")
def logout():
    # Here you could also clear cookies/sessions if you add them later
    response = RedirectResponse(url="/login", status_code=303)
    return response