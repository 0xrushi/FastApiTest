import csv
import datetime

from more_itertools import first

import models
from database import SessionLocal, engine

db = SessionLocal()

models.Base.metadata.create_all(bind=engine)

with open("data.csv", "r") as f:
    csv_reader = csv.DictReader(f)

    for row in csv_reader:
        db_record = models.Candidate(
            dob=datetime.datetime.strptime(row["dob"], "%m/%d/%Y"),
            first_name=row["first_name"],
            last_name=row["last_name"],
            ssn=row["ssn"],
        )
        db.add(db_record)

    db.commit()

db.close()