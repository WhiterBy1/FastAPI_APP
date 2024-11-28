#si genera problemas con el import de los modulos lo recomendable es poner en la terminal en windows:  set PYTHONPATH=%PYTHONPATH%;.

from fastapi import FastAPI
from models import Invoice
from db import SessionDep, create_all_tables
from sqlmodel import select
from app.routers import customers, transactions, plans

app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)

app.include_router(transactions.router)

app.include_router(plans.router)


@app.get("/")
async def root():
    return {"message": "Hello, World!"}



@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    return invoice_data
