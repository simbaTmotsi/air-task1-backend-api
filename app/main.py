from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from app.database import SessionLocal, engine
from app import models, crud, schemas
from app.routers import customers, categories, items, orders

def init_db():
    """Initialize database with test data"""
    db = SessionLocal()
    
    # Check if data already exists
    if db.query(models.Customer).first():
        db.close()
        return
    
    try:
        # Create test customers
        customers_data = [
            {"name": "John", "surname": "Doe", "email": "john.doe@example.com"},
            {"name": "Jane", "surname": "Smith", "email": "jane.smith@example.com"},
            {"name": "Bob", "surname": "Johnson", "email": "bob.johnson@example.com"},
        ]
        
        db_customers = []
        for customer_data in customers_data:
            customer = schemas.CustomerCreate(**customer_data)
            db_customer = crud.create_customer(db, customer)
            db_customers.append(db_customer)
        
        # Create test categories
        categories_data = [
            {"title": "Electronics", "description": "Electronic devices and gadgets"},
            {"title": "Clothing", "description": "Fashion and apparel items"},
            {"title": "Books", "description": "Books and educational materials"},
            {"title": "Home & Garden", "description": "Items for home and garden"},
        ]
        
        db_categories = []
        for category_data in categories_data:
            category = schemas.ShopItemCategoryCreate(**category_data)
            db_category = crud.create_category(db, category)
            db_categories.append(db_category)
        
        # Create test shop items
        items_data = [
            {"title": "Laptop", "description": "High-performance laptop", "price": 999.99, "category_ids": [1]},
            {"title": "T-Shirt", "description": "Cotton t-shirt", "price": 19.99, "category_ids": [2]},
            {"title": "Python Programming Book", "description": "Learn Python programming", "price": 39.99, "category_ids": [3]},
            {"title": "Smartphone", "description": "Latest smartphone model", "price": 699.99, "category_ids": [1]},
            {"title": "Jeans", "description": "Blue denim jeans", "price": 59.99, "category_ids": [2]},
            {"title": "Garden Tools Set", "description": "Complete set of garden tools", "price": 89.99, "category_ids": [4]},
        ]
        
        db_items = []
        for item_data in items_data:
            item = schemas.ShopItemCreate(**item_data)
            db_item = crud.create_shop_item(db, item)
            db_items.append(db_item)
        
        # Create test orders
        orders_data = [
            {
                "customer_id": db_customers[0].id,
                "items": [
                    {"shop_item_id": db_items[0].id, "quantity": 1},
                    {"shop_item_id": db_items[1].id, "quantity": 2},
                ]
            },
            {
                "customer_id": db_customers[1].id,
                "items": [
                    {"shop_item_id": db_items[3].id, "quantity": 1},
                ]
            },
            {
                "customer_id": db_customers[2].id,
                "items": [
                    {"shop_item_id": db_items[2].id, "quantity": 1},
                    {"shop_item_id": db_items[5].id, "quantity": 1},
                ]
            },
        ]
        
        for order_data in orders_data:
            order = schemas.OrderCreate(**order_data)
            crud.create_order(db, order)
            
        print("Database initialized with test data")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables
    models.Base.metadata.create_all(bind=engine)
    # Initialize database with test data
    init_db()
    yield

app = FastAPI(
    title="Online Shop API",
    description="A minimalistic backend API for an online shop",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(customers.router)
app.include_router(categories.router)
app.include_router(items.router)
app.include_router(orders.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Online Shop API", "docs": "/docs"}
