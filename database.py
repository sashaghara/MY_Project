from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

print("Creating of database ...")
Base = declarative_base()

data = "postgresql+psycopg2://postgres:200101@localhost/Item_db6"

engine=create_engine(data)


Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)