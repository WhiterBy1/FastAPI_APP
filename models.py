from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

class StatusEnum (str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    
class CustomerPlan (SQLModel, table = True):
    id: int | None = Field(default=None, primary_key=True)
    plan_id: int = Field(foreign_key= "plan.id")
    customer_id: int = Field(foreign_key= "customer.id")
    status: StatusEnum =Field(default=StatusEnum.ACTIVE)
    
class Plan (SQLModel, table = True):
    id: int | None = Field(default=None, primary_key=True)
    name:str  = Field(default=None)
    price:int = Field(default=None)
    description:str = Field(default=None)
    customer: list["Customer"] = Relationship(back_populates="plan", link_model= CustomerPlan)

class CustomerBase(SQLModel):
    name:str  = Field(default=None)
    description: str | None = Field(default=None)
    email: str = Field(default=None)
    age: int  = Field(default=None)

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class Customer(CustomerBase, table =True):
    id:int | None = Field(default=None, primary_key=True)
    transaction: list["Transaction"] = Relationship(back_populates="customer")
    plan: list["Plan"] = Relationship(back_populates="customer", link_model= CustomerPlan)
    
    

class TransactionBase(SQLModel):
    ammount: int  = Field(default=None)
    description: str = Field(default=None)

class TransactionCreate(TransactionBase):
    customer_id : int = Field(foreign_key="customer.id")

class TransactionUpdate(TransactionBase):
    pass

class Transaction(TransactionBase, table =True):
    id:int | None = Field(default=None, primary_key=True)
    customer_id : int = Field(foreign_key="customer.id")
    customer: Customer = Relationship( back_populates="transaction")

class Invoice(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction] 
    total: int 
    @property
    def total_amount(self):
        return sum(transaction.ammount for transaction in self.transactions)
    