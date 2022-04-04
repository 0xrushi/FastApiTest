from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date
from database import Base


class Record(Base):
    __tablename__ = "Records"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    country = Column(String(255), index=True)
    cases = Column(Integer)
    deaths = Column(Integer)
    recoveries = Column(Integer)

class Candidate(Base):
    __tablename__ = "Candidates"

    id = Column(Integer, primary_key=True, index=True)
    dob = Column(Date)
    first_name = Column(String(255), index=True)
    last_name = Column(String(255), index=True)
    ssn = Column(String(255), index=True)