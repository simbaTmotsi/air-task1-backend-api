from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.models import Order as OrderModel, OrderItem as OrderItemModel, Customer as CustomerModel, ShopItem as ItemModel
from app.schemas import Order, OrderCreate, OrderUpdate

router = APIRouter()

@router.post("/", response_model=Order)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    # Check if customer exists
    customer = db.query(CustomerModel).filter(CustomerModel.id == order.customer_id).first()
    if not customer:
        raise HTTPException(status_code=400, detail="Customer not found")
    
    # Create order
    db_order = OrderModel(customer_id=order.customer_id)
    db.add(db_order)
    db.flush()  # Get the order ID
    
    # Create order items
    for item_data in order.items:
        # Check if shop item exists
        shop_item = db.query(ItemModel).filter(ItemModel.id == item_data.shop_item_id).first()
        if not shop_item:
            raise HTTPException(status_code=400, detail=f"Shop item with ID {item_data.shop_item_id} not found")
        
        order_item = OrderItemModel(
            shop_item_id=item_data.shop_item_id,
            quantity=item_data.quantity,
            order_id=db_order.id
        )
        db.add(order_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/", response_model=List[Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = db.query(OrderModel).offset(skip).limit(limit).all()
    return orders

@router.get("/{order_id}", response_model=Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/{order_id}", response_model=Order)
def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    db_order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order_data = order.model_dump(exclude_unset=True)
    items_data = order_data.pop("items", None)
    
    # Update customer if provided
    if "customer_id" in order_data:
        customer = db.query(CustomerModel).filter(CustomerModel.id == order_data["customer_id"]).first()
        if not customer:
            raise HTTPException(status_code=400, detail="Customer not found")
        db_order.customer_id = order_data["customer_id"]
    
    # Update items if provided
    if items_data is not None:
        # Remove existing items
        db.query(OrderItemModel).filter(OrderItemModel.order_id == order_id).delete()
        
        # Add new items
        for item_data in items_data:
            shop_item = db.query(ItemModel).filter(ItemModel.id == item_data["shop_item_id"]).first()
            if not shop_item:
                raise HTTPException(status_code=400, detail=f"Shop item with ID {item_data['shop_item_id']} not found")
            
            order_item = OrderItemModel(
                shop_item_id=item_data["shop_item_id"],
                quantity=item_data["quantity"],
                order_id=order_id
            )
            db.add(order_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order

@router.delete("/{order_id}", response_model=dict)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}