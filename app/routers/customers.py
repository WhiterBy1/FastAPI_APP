from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from models import Customer, CustomerCreate, CustomerPlan, CustomerUpdate, Plan
from db  import SessionDep

router = APIRouter()

@router.post("/customers", response_model= Customer, tags=["customers"])
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer_db = Customer.model_validate(customer_data.model_dump())
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db

@router.get("/customers/{customer_id}", response_model= Customer, tags=["customers"])
async def get_customer(customer_id: int, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detail = "Customer not found"
            )
    return customer
@router.patch("/customers/{customer_id}", response_model = Customer, status_code= status.HTTP_201_CREATED, tags=["customers"])
async def update_customer(customer_id: int, customer_data: CustomerUpdate, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detail = "Customer not found"
            )
    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer_db.sqlmodel_update(customer_data)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db
@router.delete("/customers/{customer_id}", tags=["customers"])
async def delete_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detail = "Customer not found"
            )
    session.delete(customer_db)
    session.commit()
    return {"detail": "Customer deleted"}

@router.get("/customers", response_model= list[Customer], tags=["customers"])
async def list_customers(session: SessionDep):  
    return session.exec(select(Customer)).all()

@router.post("/customers/{customer_id}/plans/{plan_id}", tags=["customers"])
async def create_customer_to_plan(customer_id: int, plan_id: int, session: SessionDep):	
    customer_db = session.get(Customer, customer_id)
    plan_db = session.get(Plan, plan_id)
    
    if not customer_db or not plan_db:
        raise HTTPException (status_code= status.HTTP_404_NOT_FOUND, detail = "Customer or plan not found")
    
    customer_plan_db = CustomerPlan(plan_id=plan_db.id, customer_id=customer_db.id)
    
    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_plan_db)
    
    return customer_plan_db

@router.get("/customers/{customer_id}/plans", response_model= list[Plan], tags=["customers"])
async def list_customer_plans(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = "Customer not found")
    plans = customer_db.plan
    return plans

@router.delete("/customers/{customer_id}/plans/{plan_id}", tags=["customers"])
async def delete_customer_plan(customer_id: int, plan_id: int, session: SessionDep):
    customer_plan_db = session.exec(select(CustomerPlan).where(CustomerPlan.customer_id == customer_id, CustomerPlan.plan_id == plan_id)).first()
    if not customer_plan_db:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = "Customer plan not found")
    session.delete(customer_plan_db)
    session.commit()
    return {"detail": "Customer plan deleted"}
