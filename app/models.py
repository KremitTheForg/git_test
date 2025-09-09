from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
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

    # Link to User
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="candidates")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Reverse relationship (one-to-many)
    candidates = relationship("Candidate", back_populates="user", cascade="all, delete-orphan")
