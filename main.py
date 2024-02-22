from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import func, asc, desc
from sqlalchemy.orm import Session, selectinload
from models import Client, Treatment, Doctor
from database import Base, engine, SessionLocal
from pydantic import BaseModel
from datetime import date
from typing import List


"""""
class Item(BaseModel):
    id:int
    name:str
    description:str
    on_offer:bool
"""""
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ClientCreate(BaseModel):
    full_name: str
    date_of_birth: date
    policy_number: int
    social_status: str


class ClientResponse(BaseModel):
    id: int
    full_name: str
    date_of_birth: date
    policy_number: int
    social_status: str


class ClientDelete(BaseModel):
    message: str


# Pydantic model for Result
class TreatmentCreate(BaseModel):
    diagnosis: str
    current_state: str
    date_start: date
    date_end: date
    Client_id: int
    doctor_id: int


class TreatmentResponse(BaseModel):
    id: int
    diagnosis: str
    current_state: str
    date_start: date
    date_end: date
    Client_id: int
    doctor_id: int


class TreatmentDelete(BaseModel):
    message: str


# Pydantic model for Athlete
class DoctorCreate(BaseModel):
    full_name: str
    speciality: str
    exp_years: int


class DoctorResponse(BaseModel):
    id: int
    full_name: str
    speciality: str
    exp_years: int


class DoctorDelete(BaseModel):
    message: str


@app.post("/Client/", response_model=ClientResponse)
def create_Client(Client_: ClientCreate, db: Session = Depends(get_db)):
    db_Client = Client(**Client_.model_dump())
    db.add(db_Client)
    db.commit()
    db.refresh(db_Client)
    return db_Client


@app.post("/treatment/", response_model=TreatmentResponse)
def create_treatment(treatment: TreatmentCreate, db: Session = Depends(get_db)):
    db_treatment = Treatment(**treatment.model_dump())
    db.add(db_treatment)
    db.commit()
    db.refresh(db_treatment)
    Client = db.query(Client).filter(Client.id == treatment.Client_id).first() # noqa
    if Client is not None:
        Client.doctor_id = treatment.doctor_id
        db.commit()

    return db_treatment

@app.post("/doctor/", response_model=DoctorResponse)
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    db_doctor = Doctor(**doctor.model_dump())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


# Read
@app.get("/Client/{Client_id}", response_model=ClientResponse)
def get_Client(Client_id: int, db: Session = Depends(get_db)):
    Client = db.query(Client).filter(Client.id == Client_id).first() # noqa
    if Client is None:
        raise HTTPException(status_code=404, detail='Client not found')
    return Client


@app.get("/doctor/{doctor_id}", response_model=DoctorResponse)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first() # noqa
    if doctor is None:
        raise HTTPException(status_code=404, detail='doctor not found')
    return doctor


@app.get("/treatment/{treatment_id}", response_model=TreatmentResponse)
def get_treatment(treatment_id: int, db: Session = Depends(get_db)):
    treatment = db.query(Treatment).filter(Treatment.id == treatment_id).first() # noqa
    if treatment is None:
        raise HTTPException(status_code=404, detail='Treatment not found')
    return treatment

# Update
@app.put("/Client/{Client_id}", response_model=ClientResponse)
def update_Client(Client_id: int, updated: ClientCreate, db: Session = Depends(get_db)):
    Client = db.query(Client).filter(Client.id == Client_id).first() # noqa
    if Client is None:
        raise HTTPException(status_code=404, detail='Client not found')

    for key, value in updated.model_dump().items():
        setattr(Client, key, value)

    db.commit()
    db.refresh(Client)
    return Client


@app.put("/treatment/{treatment_id}", response_model=TreatmentResponse)
def update_treatment(treatment_id: int, updated: TreatmentCreate, db: Session = Depends(get_db)):
    treatment = db.query(Treatment).filter(Treatment.id == treatment_id).first() # noqa
    if treatment is None:
        raise HTTPException(status_code=404, detail='Treatment not found')

    for key, value in updated.model_dump().items():
        setattr(treatment, key, value)

    db.commit()
    db.refresh(treatment)
    return treatment


@app.put("/doctor/{doctor_id}", response_model=doctorResponse)
def update_doctor(doctor_id: int, updated: DoctorCreate, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first() # noqa
    if doctor is None:
        raise HTTPException(status_code=404, detail="doctor not found")

    for key, value in updated.model_dump().items():
        setattr(doctor, key, value)

    db.commit()
    db.refresh(doctor)
    return doctor


# Delete
@app.delete("/Client/{Client_id}", response_model=ClientDelete)
def delete_Client(Client_id: int, db: Session = Depends(get_db)):
    Client = db.query(Client).filter(Client.id == Client_id).first() # noqa
    if Client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    db.delete(Client)
    db.commit()
    return {"message": "Client deleted"}


@app.delete("/treatment/{treatment_id}", response_model=TreatmentDelete)
def delete_treatment(treatment_id: int, db: Session = Depends(get_db)):
    treatment = db.query(Treatment).filter(Treatment.id == treatment_id).first() # noqa
    if treatment is None:
        raise HTTPException(status_code=404, detail="Treatment not found")

    db.delete(treatment)
    db.commit()
    return {"message": "Treatment deleted"}


@app.delete("/doctor/{doctor_id}", response_model=DoctorDelete)
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first() # noqa
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")


    db.delete(Doctor)
    db.commit()
    return {"message": "Doctor deleted"}


# Read with pagination
@app.get("/Client/", response_model=List[ClientResponse])
def get_Client(page: int = 0, per_page: int = 10, db: Session = Depends(get_db)):
    Client_ = db.query(Client).offset(page).limit(per_page).all()
    return Client_


@app.get("/treatment/", response_model=List[TreatmentResponse])
def get_treatment(page: int = 0, per_page: int = 10, db: Session = Depends(get_db)):
    treatment = db.query(Treatment).offset(page).limit(per_page).all()
    return treatment


@app.get("/doctor/", response_model=List[DoctorResponse])
def get_doctor_sorted(page: int = 0, per_page: int = 10, sort_by: str = "id", db: Session = Depends(get_db)):
    doctor = db.query(Doctor).order_by(getattr(Doctor, sort_by)).offset(page).limit(per_page).all()
    return doctor

# SELECT... WHERE


@app.get("/api/Clients/search", response_model=List[ClientResponse])
def search_Clients(diagnosis: str, current_state: str, db: Session = Depends(get_db)):
    Clients = db.query(Client).filter(Treatment.diagnosis == diagnosis, # noqa
                                        Treatment.current_state == current_state).all() # noqa
    if not Clients:
        raise HTTPException(status_code=404, detail="No matches found")
    return Clients

# JOIN


@app.get("/api/Clients_with_doctor/", response_model=List[dict])
def get_Clients_with_doctor(db: Session = Depends(get_db)):
    Clients_with_doctor = db.query(Client).options(selectinload(Client.doctor)).all()
    Clients_data = []
    for Client_ in Clients_with_doctor:
        if Client_.doctor is not None:
            Clients_data.append({
                "id": Client_.id,
                "name": Client_.full_name,
                "doctor": {
                    "id": Client_.doctor.id,
                    "name": Client_.doctor.full_name,
                    "specialty": Client_.doctor.speciality,
                }
            })
    return Clients_data

# UPDATE


@app.put("/api/treatments/update_by_conditions/{diagnosis}/{current_state}", response_model=TreatmentResponse)
def update_treatment_by_conditions(diagnosis: str, current_state: str, updated: TreatmentCreate,
                                   db: Session = Depends(get_db)):
    treatment = db.query(Treatment).filter(Treatment.diagnosis == diagnosis, # noqa
                                           Treatment.current_state == current_state).first() # noqa
    if treatment is None:
        raise HTTPException(status_code=404, detail='Treatment not found')

    for key, value in updated.model_dump().items():
        if updated.Client_id != 0:
            setattr(treatment, key, value)

    db.commit()
    db.refresh(treatment)
    return treatment

# GROUP BY


@app.get("/api/treatments/stats", response_model=dict)
def get_treatments_stats(db: Session = Depends(get_db)):
    result = db.query(Treatment.diagnosis,
                      func.count(Treatment.id).label('treatment_count')).group_by(Treatment.diagnosis).all()
    return {row[0]: row[1] for row in result}

# SORT


@app.get("/api/Clients", response_model=List[ClientResponse])
def get_sorted_Clients(sort_by: str, order: str, db: Session = Depends(get_db)):
    if order.lower() not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order parameter. Use "asc" or "desc".')

    sort_column = getattr(Client, sort_by, None)
    if sort_column is None:
        raise HTTPException(status_code=400, detail='Invalid sort_by parameter.')

    Clients_ = db.query(Client).order_by(asc(sort_column) if order.lower() == 'asc' else desc(sort_column)).all()
    return Clients_

# ORM

# CREATE


new_Client = Client(full_name='John Doe', date_of_birth='1990-01-01', policy_number=123456, social_status='Active')
session.add(new_Client)
session.commit()

# READ
Clients = session.query(Client).all()
for Client in Clients:
    print(Client.full_name, Client.date_of_birth)

# UPD
Client_to_update = session.query(Client).filter_by(full_name='John Doe').first()
Client_to_update.social_status = 'Inactive'
session.commit()

# DELETE
Client_to_delete = session.query(Client).filter_by(full_name='John Doe').first()
session.delete(Client_to_delete)
session.commit()

Doctor