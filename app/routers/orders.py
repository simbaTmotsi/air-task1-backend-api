from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    # Check if customer exists
    customer = crud.get_customer(db, customer_id=order.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Check if all shop items exist
    for item in order.items:
        shop_item = crud.get_shop_item(db, item_id=item.shop_item_id)
        if not shop_item:
            raise HTTPException(status_code=404, detail=f"Shop item with id {item.shop_item_id} not found")
    
    return crud.create_order(db=db, order=order)

@router.get("/", response_model=List[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders

@router.get("/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.put("/{order_id}", response_model=schemas.Order)
def update_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    # Check if customer exists (if customer_id is being updated)
    if order.customer_id is not None:
        customer = crud.get_customer(db, customer_id=order.customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
    
    # Check if all shop items exist (if items are being updated)
    if order.items is not None:
        for item in order.items:
            shop_item = crud.get_shop_item(db, item_id=item.shop_item_id)
            if not shop_item:
                raise HTTPException(status_code=404, detail=f"Shop item with id {item.shop_item_id} not found")
    
    db_order = crud.update_order(db, order_id=order_id, order=order)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.delete("/{order_id}", response_model=schemas.Order)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.delete_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order
