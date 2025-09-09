from fastapi import APIRouter, Depends, HTTPException, Request   # 👈 added Request
from sqlalchemy.orm import Session
from app import schemas, crud, database

router = APIRouter(
    prefix="/api/v1/hr/recruitment/candidates",
    tags=["candidates"]
)

@router.post("/", response_model=schemas.CandidateOut)
def create_candidate(
    request: Request,
    candidate: schemas.CandidateCreate,
    db: Session = Depends(database.get_db)
):
    user = request.session.get("user")
    user_id = user["id"] if user else None
    return crud.create_candidate(db=db, candidate=candidate, user_id=user_id)

@router.get("/{candidate_id}", response_model=schemas.CandidateOut)
def read_candidate(candidate_id: int, db: Session = Depends(database.get_db)):
    db_candidate = crud.get_candidate(db, candidate_id=candidate_id)
    if not db_candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return db_candidate

@router.get("/", response_model=list[schemas.CandidateOut])
def read_candidates(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return crud.get_candidates(db, skip=skip, limit=limit)
