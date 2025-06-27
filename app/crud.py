from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas

# Customer CRUD operations
def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_customer_by_email(db: Session, email: str):
    return db.query(models.Customer).filter(models.Customer.email == email).first()

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).offset(skip).limit(limit).all()

def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, customer_id: int, customer: schemas.CustomerUpdate):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if db_customer:
        update_data = customer.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_customer, field, value)
        db.commit()
        db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: int):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if db_customer:
        db.delete(db_customer)
        db.commit()
    return db_customer

# ShopItemCategory CRUD operations
def get_category(db: Session, category_id: int):
    return db.query(models.ShopItemCategory).filter(models.ShopItemCategory.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ShopItemCategory).offset(skip).limit(limit).all()

def create_category(db: Session, category: schemas.ShopItemCategoryCreate):
    db_category = models.ShopItemCategory(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category: schemas.ShopItemCategoryUpdate):
    db_category = db.query(models.ShopItemCategory).filter(models.ShopItemCategory.id == category_id).first()
    if db_category:
        update_data = category.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_category, field, value)
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = db.query(models.ShopItemCategory).filter(models.ShopItemCategory.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category

# ShopItem CRUD operations
def get_shop_item(db: Session, item_id: int):
    return db.query(models.ShopItem).filter(models.ShopItem.id == item_id).first()

def get_shop_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ShopItem).offset(skip).limit(limit).all()

def create_shop_item(db: Session, item: schemas.ShopItemCreate):
    db_item = models.ShopItem(
        title=item.title,
        description=item.description,
        price=item.price
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    # Add categories
    if item.category_ids:
        categories = db.query(models.ShopItemCategory).filter(
            models.ShopItemCategory.id.in_(item.category_ids)
        ).all()
        db_item.categories = categories
        db.commit()
        db.refresh(db_item)
    
    return db_item

def update_shop_item(db: Session, item_id: int, item: schemas.ShopItemUpdate):
    db_item = db.query(models.ShopItem).filter(models.ShopItem.id == item_id).first()
    if db_item:
        update_data = item.model_dump(exclude_unset=True)
        category_ids = update_data.pop('category_ids', None)
        
        for field, value in update_data.items():
            setattr(db_item, field, value)
        
        if category_ids is not None:
            categories = db.query(models.ShopItemCategory).filter(
                models.ShopItemCategory.id.in_(category_ids)
            ).all()
            db_item.categories = categories
        
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_shop_item(db: Session, item_id: int):
    db_item = db.query(models.ShopItem).filter(models.ShopItem.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

# Order CRUD operations
def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()

def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(customer_id=order.customer_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Add order items
    for item_data in order.items:
        db_order_item = models.OrderItem(
            shop_item_id=item_data.shop_item_id,
            quantity=item_data.quantity,
            order_id=db_order.id
        )
        db.add(db_order_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order(db: Session, order_id: int, order: schemas.OrderUpdate):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        update_data = order.model_dump(exclude_unset=True)
        items_data = update_data.pop('items', None)
        
        # Update basic fields
        for field, value in update_data.items():
            setattr(db_order, field, value)
        
        # Update items if provided
        if items_data is not None:
            # Delete existing order items
            db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).delete()
            
            # Add new order items
            for item_data in items_data:
                db_order_item = models.OrderItem(
                    shop_item_id=item_data["shop_item_id"],
                    quantity=item_data["quantity"],
                    order_id=order_id
                )
                db.add(db_order_item)
        
        db.commit()
        db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        # Load relationships before deletion to avoid DetachedInstanceError
        _ = db_order.customer
        _ = db_order.items
        for item in db_order.items:
            _ = item.shop_item
        
        db.delete(db_order)
        db.commit()
    return db_order
