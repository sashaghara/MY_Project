from sqlalchemy.orm import Session
from faker import Faker
from models import Client, Treatment, Doctor
from datetime import date, timedelta

fake = Faker()



def populate(db: Session):
    for _ in range(10):
        doctor = Doctor(
            full_name=fake.name(),
            speciality=fake.job(),
            exp_years=fake.random_int(min=1, max=20)
        )
        db.add(doctor)
        db.commit()


    for _ in range(100):
        client = Client(
            full_name=fake.name(),
            date_of_birth=fake.date_of_birth(),
            policy_number=fake.random_int(min=100000, max=999999),
            social_status=fake.random_element(elements=('Active', 'Inactive'))
        )
        db.add(client)
        db.commit()

        treatment = Treatment(
            diagnosis=fake.word(),
            current_state=fake.word(),
            date_start=fake.date_between(start_date='-30d', end_date='today'),
            date_end=fake.date_between_dates(date_start=treatment.date_start, end_date=treatment.date_start + timedelta(days=30)),
            client_id=client.id,
            doctor_id=fake.random_int(min=1, max=10) 
        )
        db.add(treatment)
        db.commit()

    print("Database populated successfully.")
