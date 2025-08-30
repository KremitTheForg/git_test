from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, database

router = APIRouter(
    prefix="/api/v1/hr/recruitment/candidates",
    tags=["candidates"]
)

@router.post("/", response_model=schemas.CandidateOut)
def create_candidate(candidate: schemas.CandidateCreate, db: Session = Depends(database.get_db)):
    return crud.create_candidate(db=db, candidate=candidate)

@router.get("/{candidate_id}", response_model=schemas.CandidateOut)
def read_candidate(candidate_id: int, db: Session = Depends(database.get_db)):
    db_candidate = crud.get_candidate(db, candidate_id=candidate_id)
    if not db_candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return db_candidate

@router.get("/", response_model=list[schemas.CandidateOut])
def read_candidates(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return crud.get_candidates(db, skip=skip, limit=limit)
