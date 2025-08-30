from sqlalchemy.orm import Session
from . import models, schemas

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
