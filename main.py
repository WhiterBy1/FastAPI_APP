from fastapi import FastAPI, HTTPException, status
from models import CustomerCreate, Transaction, Invoice, Customer, CustomerUpdate
from db import SessionDep, create_all_tables
from sqlmodel import select

app = FastAPI(lifespan=create_all_tables)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

db_customers: list[Customer] = []
@app.post("/customers", response_model= Customer)
async def create_customer(customer_data: CustomerUpdate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@app.get("/customers/{customer_id}", response_model= Customer)
async def get_customer(customer_id: int, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detaill = "Customer not found"
            )
    return customer
@app.patch("/customers/{customer_id}", response_model = Customer, status_code= status.HTTP_201_CREATED)
async def update_customer(customer_id: int, customer_data: CustomerCreate, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detaill = "Customer not found"
            )
    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer.sqlmodel_update(customer_data)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer
@app.delete("/customers/{customer_id}")
async def delete_customer(customer_id: int, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detaill = "Customer not found"
            )
    session.delete(customer)
    session.commit()
    return {"detail": "Customer deleted"}

@app.get("/customers", response_model= list[Customer])
async def list_customers(session: SessionDep):  
    return session.exec(select(Customer)).all()

@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    return invoice_data

