from typing import Annotated
from fastapi import FastAPI,Depends
from sqlmodel import Session, create_engine, SQLModel

DATABASE_NAME = 'db.sqlite3'
DATABASE_URL = f"sqlite:///{DATABASE_NAME}"

engine = create_engine(DATABASE_URL)

def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield 

def get_session():
    with Session(engine) as session:
        #usando Programacion orientada asincrona
        yield session #se usa cuando se necesite

SessionDep = Annotated[Session, Depends(get_session)]

