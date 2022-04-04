from pyexpat import model
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from sqlalchemy.sql import func

import models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def main():
    return RedirectResponse(url="/docs/")


@app.get("/records/", response_model=List[schemas.Record])
def show_records(db: Session = Depends(get_db)):
    records = db.query(models.Record).all()
    return records

@app.get("/candidates/", response_model=List[schemas.Candidate])
def show_candidates(db: Session = Depends(get_db)):
    records = db.query(models.Candidate).all()
    return records

@app.get("/candidates2/", response_model=List[schemas.Candidate])
def show_candidates(db: Session = Depends(get_db)):
    records = db.query(models.Candidate).filter(func.substr(models.Candidate.last_name,0,2) == "p").all()
    return records    

@app.delete("/candidates/{ca_id}")
def delete_candidates(ca_id: int, db: Session = Depends(get_db)):
    stm = db.query(models.Candidate).filter(models.Candidate.id == ca_id).delete()
    print(stm)
    db.commit()
    return  {"cat_deleted": stm}

@app.post("/candidates/")
async def create_item(candidate: schemas.Candidate, db: Session = Depends(get_db)):
    c = models.Candidate(**candidate.dict())
    db.add(c)
    db.commit()
    return candidate

@app.put("/candidates/{cand_id}")
async def update_item(cand_id: int, candidate: schemas.Candidate, db: Session = Depends(get_db)):
    db_item = db.query(models.Candidate).filter(models.Candidate.id == cand_id).one_or_none()
    if db_item:
        db_item.ssn = candidate.ssn
        db_item.first_name = candidate.first_name
        db_item.last_name = candidate.last_name
        db_item.id = candidate.id
        db.add(db_item)
        db.commit()
        return True
    return False