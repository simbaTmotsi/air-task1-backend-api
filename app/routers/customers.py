from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.models import Customer as CustomerModel
from app.schemas import Customer, CustomerCreate, CustomerUpdate

router = APIRouter()

@router.post("/", response_model=Customer)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    db_customer = db.query(CustomerModel).filter(CustomerModel.email == customer.email).first()
    if db_customer:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_customer = CustomerModel(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.get("/", response_model=List[Customer])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = db.query(CustomerModel).offset(skip).limit(limit).all()
    return customers

@router.get("/{customer_id}", response_model=Customer)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(CustomerModel).filter(CustomerModel.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.put("/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = db.query(CustomerModel).filter(CustomerModel.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Check if email is being updated and if it already exists
    if customer.email and customer.email != db_customer.email:
        existing_customer = db.query(CustomerModel).filter(CustomerModel.email == customer.email).first()
        if existing_customer:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    customer_data = customer.model_dump(exclude_unset=True)
    for field, value in customer_data.items():
        setattr(db_customer, field, value)
    
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.delete("/{customer_id}", response_model=dict)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(CustomerModel).filter(CustomerModel.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db.delete(customer)
    db.commit()
    return {"message": "Customer deleted successfully"}