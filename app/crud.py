from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

def create_candidate(db: Session, candidate: schemas.CandidateCreate):
    db_candidate = models.Candidate(
        first_name=candidate.first_name,
        last_name=candidate.last_name,
        email=candidate.email,
        mobile=candidate.mobile,
        job_title=candidate.job_title,
        address=candidate.address,
        status="Applied"
    )
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

def get_candidate(db: Session, candidate_id: int):
    return db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()

def get_candidates(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Candidate).offset(skip).limit(limit).all()

##

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()