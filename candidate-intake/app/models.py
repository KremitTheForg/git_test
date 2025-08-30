from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from .database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    mobile = Column(String, nullable=True)
    job_title = Column(String, nullable=True)
    address = Column(String, nullable=True)

    status = Column(String, default="Applied")  # default status
    applied_on = Column(DateTime(timezone=True), server_default=func.now())
