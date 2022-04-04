from datetime import date
from pydantic import BaseModel


class Record(BaseModel):
    id: int
    date: date
    country: str
    cases: int
    deaths: int
    recoveries: int

    class Config:
        orm_mode = True

class Candidate(BaseModel):
    id: int
    dob: date
    first_name: str
    last_name: str
    ssn: str

    class Config:
        orm_mode = True