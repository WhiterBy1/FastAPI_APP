from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from models import Customer, CustomerCreate, CustomerUpdate
from db  import SessionDep

router = APIRouter()

@router.post("/customers", response_model= Customer, tags=["customers"])
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@router.get("/customers/{customer_id}", response_model= Customer, tags=["customers"])
async def get_customer(customer_id: int, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detaill = "Customer not found"
            )
    return customer
@router.patch("/customers/{customer_id}", response_model = Customer, status_code= status.HTTP_201_CREATED, tags=["customers"])
async def update_customer(customer_id: int, customer_data: CustomerUpdate, session: SessionDep):
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
@router.delete("/customers/{customer_id}", tags=["customers"])
async def delete_customer(customer_id: int, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detaill = "Customer not found"
            )
    session.delete(customer)
    session.commit()
    return {"detail": "Customer deleted"}

@router.get("/customers", response_model= list[Customer], tags=["customers"])
async def list_customers(session: SessionDep):  
    return session.exec(select(Customer)).all()
