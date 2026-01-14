from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "postgresql+psycopg2://postgres:sua_senha@localhost:5432/precocombustiveis"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

def create_tables():
    Base.metadata.create_all(engine) #type:ignore
