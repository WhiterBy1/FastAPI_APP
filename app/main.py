from fastapi import FastAPI
from models import  Transaction, Invoice
from db import SessionDep, create_all_tables
from sqlmodel import select
from app.routers import customers


app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)
@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    return invoice_data

