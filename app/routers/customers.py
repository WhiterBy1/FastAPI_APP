from fastapi import APIRouter, HTTPException, status, Query, Depends
from sqlmodel import select
from fastapi_featureflags import FeatureFlags, feature_enabled
from models import Customer, CustomerCreate, CustomerPlan, CustomerUpdate, Plan, StatusEnum
from db import SessionDep

# Inicializar las feature flags 
FeatureFlags.load_conf_from_json("app/routers/flags/feature_flags.json")

router = APIRouter()

# Crear cliente
@router.post("/customers", response_model=Customer, tags=["customers"])
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    if not feature_enabled("enable_create_customer"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Feature 'Create Customer' is disabled"
        )
    customer_db = Customer.model_validate(customer_data.model_dump())
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db

# Obtener cliente por ID
@router.get("/customers/{customer_id}", response_model=Customer, tags=["customers"])
async def get_customer(customer_id: int, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Customer not found"
        )
    return customer

# Actualizar cliente
@router.patch("/customers/{customer_id}", response_model=Customer, tags=["customers"])
async def update_customer(customer_id: int, customer_data: CustomerUpdate, session: SessionDep):
    if not feature_enabled("enable_update_customer"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Feature 'Update Customer' is disabled"
        )
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Customer not found"
        )
    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer_db.sqlmodel_update(customer_data)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db

# Eliminar cliente
@router.delete("/customers/{customer_id}", tags=["customers"])
async def delete_customer(customer_id: int, session: SessionDep):
    if not feature_enabled("enable_delete_customer"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Feature 'Delete Customer' is disabled"
        )
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Customer not found"
        )
    session.delete(customer_db)
    session.commit()
    return {"detail": "Customer deleted"}

# Listar clientes
@router.get("/customers", response_model=list[Customer], tags=["customers"])
async def list_customers(session: SessionDep):  
    return session.exec(select(Customer)).all()

# Crear relación entre cliente y plan
@router.post("/customers/{customer_id}/plans/{plan_id}", tags=["customers"])
async def create_customer_to_plan(customer_id: int, plan_id: int, session: SessionDep, planstatus: StatusEnum = Query()):
    if not feature_enabled("enable_create_customer_plan"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Feature 'Create Customer Plan' is disabled"
        )
    customer_db = session.get(Customer, customer_id)
    plan_db = session.get(Plan, plan_id)
    
    if not customer_db or not plan_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Customer or plan not found"
        )
    
    customer_plan_db = CustomerPlan(plan_id=plan_db.id, customer_id=customer_db.id, planstatus=planstatus)
    
    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_plan_db)
    
    return customer_plan_db

# Listar planes de un cliente
@router.get("/customers/{customer_id}/plans", response_model=list[Plan], tags=["customers"])
async def list_customer_plans(customer_id: int, session: SessionDep, planstatus: StatusEnum = Query()):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    query = (select(CustomerPlan)
            .where(CustomerPlan.customer_id == customer_id)
            .where(CustomerPlan.status == planstatus))
    plans = session.exec(query).all()
    return plans

# Eliminar relación entre cliente y plan
@router.delete("/customers/{customer_id}/plans/{plan_id}", tags=["customers"])
async def delete_customer_plan(customer_id: int, plan_id: int, session: SessionDep):
    if not feature_enabled("enable_delete_customer_plan"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Feature 'Delete Customer Plan' is disabled"
        )
    customer_plan_db = session.exec(select(CustomerPlan).where(
        CustomerPlan.customer_id == customer_id, 
        CustomerPlan.plan_id == plan_id)).first()
    if not customer_plan_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Customer plan not found"
        )
    session.delete(customer_plan_db)
    session.commit()
    return {"detail": "Customer plan deleted"}

# Recargar feature flags
@router.post("/reload-feature-flags", tags=["admin"])
async def reload_feature_flags():
    FeatureFlags.reload_feature_flags()
    return {"detail": "Feature flags reloaded"}
