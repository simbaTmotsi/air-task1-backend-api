from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.models import ShopItem as ItemModel, ShopItemCategory as CategoryModel
from app.schemas import ShopItem, ShopItemCreate, ShopItemUpdate

router = APIRouter()

@router.post("/", response_model=ShopItem)
def create_item(item: ShopItemCreate, db: Session = Depends(get_db)):
    item_data = item.model_dump()
    category_ids = item_data.pop("category_ids", [])
    
    db_item = ItemModel(**item_data)
    
    # Add categories if provided
    if category_ids:
        categories = db.query(CategoryModel).filter(CategoryModel.id.in_(category_ids)).all()
        if len(categories) != len(category_ids):
            raise HTTPException(status_code=400, detail="One or more categories not found")
        db_item.categories = categories
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=List[ShopItem])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(ItemModel).offset(skip).limit(limit).all()
    return items

@router.get("/{item_id}", response_model=ShopItem)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=ShopItem)
def update_item(item_id: int, item: ShopItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item_data = item.model_dump(exclude_unset=True)
    category_ids = item_data.pop("category_ids", None)
    
    # Update basic fields
    for field, value in item_data.items():
        setattr(db_item, field, value)
    
    # Update categories if provided
    if category_ids is not None:
        categories = db.query(CategoryModel).filter(CategoryModel.id.in_(category_ids)).all()
        if len(categories) != len(category_ids):
            raise HTTPException(status_code=400, detail="One or more categories not found")
        db_item.categories = categories
    
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}", response_model=dict)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}