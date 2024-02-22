from sqlalchemy import Column, Integer, String, Date, ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from database import Base, engine



class Client(Base):
    __tablename__ = 'Client'
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(255),nullable = False)
    born = Column(Date, nullable=False)
    social_number = Column(Integer, nullable = False)
    social_status = Column(String(255), nullable = False)

    treatments = relationship('Treatment', back_populates='Client')

    Doctor_id = Column(Integer, ForeignKey('Doctor.id'))
    Doctor = relationship("Doctor", back_populates="Clients")

    search_data = Column(JSONB, nullable=True)


class Treatment(Base):
    __tablename__ = 'treatments'

    id = Column(Integer, primary_key=True, index=True)
    diagnosis = Column(String(150), nullable=False)
    current_state = Column(String(150), nullable=False)
    date_start = Column(Date, nullable=False)
    date_end = Column(Date, nullable=False)
    # N --> 1
    Client_id = Column(Integer, ForeignKey('Client.id', ondelete='CASCADE'), nullable=False)
    Client = relationship('Client', back_populates='treatments')
    # N --> 1
    Doctor_id = Column(Integer, ForeignKey('Doctor.id', ondelete='CASCADE'), nullable=False)
    Doctors = relationship('Doctor', secondary='Therapist', back_populates='treatments')


class Doctor(Base):
    __tablename__ = 'Doctor'

    id = Column(Integer, primary_key= True, index = True)
    name = Column(String(255), nullable = False, unique = True)
    specialization = Column(String(255), nullable = False)
    experience = Column(Integer, nullable = True)

    treatments = relationship('Treatment', secondary='Therapist', back_populates='Doctors')

    Client = relationship("Client", back_populates="Doctor")




class TreatmentDoctor(Base):
    __tablename__ = 'Therapist'

    treatment_id = Column(Integer, ForeignKey('treatments.id', ondelete='CASCADE'), primary_key=True)
    Doctor_id = Column(Integer, ForeignKey('Doctor.id', ondelete='CASCADE'), primary_key=True)



Index('ix_treatments_id', Treatment.id, unique=False, postgresql_using='gin').create(bind=engine, checkfirst=True)

Base.metadata.create_all(bind=engine)


