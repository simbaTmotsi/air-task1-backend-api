from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.models import ShopItemCategory as CategoryModel
from app.schemas import ShopItemCategory, ShopItemCategoryCreate, ShopItemCategoryUpdate

router = APIRouter()

@router.post("/", response_model=ShopItemCategory)
def create_category(category: ShopItemCategoryCreate, db: Session = Depends(get_db)):
    db_category = CategoryModel(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("/", response_model=List[ShopItemCategory])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = db.query(CategoryModel).offset(skip).limit(limit).all()
    return categories

@router.get("/{category_id}", response_model=ShopItemCategory)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=ShopItemCategory)
def update_category(category_id: int, category: ShopItemCategoryUpdate, db: Session = Depends(get_db)):
    db_category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    category_data = category.model_dump(exclude_unset=True)
    for field, value in category_data.items():
        setattr(db_category, field, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/{category_id}", response_model=dict)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}