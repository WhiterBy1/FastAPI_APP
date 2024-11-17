from fastapi import APIRouter, HTTPException, status
from models import Plan
from sqlmodel import select

from db import SessionDep

router = APIRouter()

@router.post("/plans", tags=["plan"])
def create_plan(plan_data: Plan, session: SessionDep):
    plan_db = Plan.model_validate(plan_data.model_dump())
    session.add(plan_db)
    session.commit()
    session.refresh(plan_db)
    return plan_db

@router.get("/plans", tags=["plan"])
def get_plans(session: SessionDep):
    return session.exec(select(Plan)).all()

@router.get("/plans/{plan_id}", tags=["plan"])
def get_plan(plan_id: int, session: SessionDep):
    plan = session.get(Plan, plan_id)
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    return plan



@router.delete("/plans/{plan_id}", tags=["plan"])
def delete_plan(plan_id: int, session: SessionDep):
    plan = session.get(Plan, plan_id)
    if not plan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    session.delete(plan)
    session.commit()
    return {"detail": "Plan deleted"}