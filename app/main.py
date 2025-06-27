from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine
from app.models.models import Base
from app.routers import customers, categories, items, orders
from app.init_data import create_test_data

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize test data on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_test_data()
    yield
    # Shutdown (no cleanup needed)

app = FastAPI(
    title="Online Shop API",
    description="A minimalistic backend web app for an online shop",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(customers.router, prefix="/customers", tags=["customers"])
app.include_router(categories.router, prefix="/categories", tags=["categories"])
app.include_router(items.router, prefix="/items", tags=["items"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Online Shop API"}