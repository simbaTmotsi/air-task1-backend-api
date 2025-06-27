# Online Shop API

A minimalistic backend web application for an online shop built with FastAPI, SQLAlchemy, and SQLite.

## Features

- Full CRUD APIs for:
  - **Customers** - Manage customer information
  - **Shop Item Categories** - Organize products into categories
  - **Shop Items** - Manage product catalog with many-to-many category relationships
  - **Orders** - Handle customer orders with multiple items
- Automatic API documentation with Swagger UI
- Comprehensive test suite with pytest
- SQLite database with automatic table creation
- Test data initialization on startup

## Data Entities

### Customer
- ID (integer, auto-generated)
- Name (string)
- Surname (string)
- Email (string, unique)

### ShopItemCategory
- ID (integer, auto-generated)
- Title (string)
- Description (string)

### ShopItem
- ID (integer, auto-generated)
- Title (string)
- Description (string)
- Price (float)
- Categories (many-to-many relationship with ShopItemCategory)

### Order
- ID (integer, auto-generated)
- Customer (foreign key to Customer)
- Items (list of OrderItem)

### OrderItem
- ID (integer, auto-generated)
- ShopItem (foreign key to ShopItem)
- Quantity (integer)
- Order (foreign key to Order)

## Project Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository** (if using git):
   ```bash
   cd /Users/simbatmotsi/Documents/Projects/air-task1-backend-api
   ```

2. **Create and activate a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive API Documentation (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Documentation (ReDoc)**: http://localhost:8000/redoc

### Test Data
The application automatically creates test data on startup including:
- 3 sample customers
- 4 product categories (Electronics, Books, Clothing, Home & Garden)
- 5 sample products
- 2 sample orders with items

## API Endpoints

### Customers
- `POST /customers/` - Create a new customer
- `GET /customers/` - Get all customers (with pagination)
- `GET /customers/{customer_id}` - Get customer by ID
- `PUT /customers/{customer_id}` - Update customer
- `DELETE /customers/{customer_id}` - Delete customer

### Categories
- `POST /categories/` - Create a new category
- `GET /categories/` - Get all categories (with pagination)
- `GET /categories/{category_id}` - Get category by ID
- `PUT /categories/{category_id}` - Update category
- `DELETE /categories/{category_id}` - Delete category

### Shop Items
- `POST /items/` - Create a new item
- `GET /items/` - Get all items (with pagination)
- `GET /items/{item_id}` - Get item by ID
- `PUT /items/{item_id}` - Update item
- `DELETE /items/{item_id}` - Delete item

### Orders
- `POST /orders/` - Create a new order
- `GET /orders/` - Get all orders (with pagination)
- `GET /orders/{order_id}` - Get order by ID
- `PUT /orders/{order_id}` - Update order
- `DELETE /orders/{order_id}` - Delete order

## Running Tests

### Run all tests:
```bash
pytest
```

### Run tests with verbose output:
```bash
pytest -v
```

### Run tests for a specific module:
```bash
pytest tests/test_customers.py -v
pytest tests/test_categories.py -v
pytest tests/test_items.py -v
pytest tests/test_orders.py -v
```

### Run tests with coverage:
```bash
pytest --cov=app tests/
```

## Example Usage

### Creating a Customer
```bash
curl -X POST "http://localhost:8000/customers/" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John",
       "surname": "Doe", 
       "email": "john.doe@example.com"
     }'
```

### Creating a Category
```bash
curl -X POST "http://localhost:8000/categories/" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Electronics",
       "description": "Electronic devices and gadgets"
     }'
```

### Creating a Shop Item
```bash
curl -X POST "http://localhost:8000/items/" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Smartphone",
       "description": "Latest model smartphone",
       "price": 599.99,
       "category_ids": [1]
     }'
```

### Creating an Order
```bash
curl -X POST "http://localhost:8000/orders/" \
     -H "Content-Type: application/json" \
     -d '{
       "customer_id": 1,
       "items": [
         {
           "shop_item_id": 1,
           "quantity": 2
         }
       ]
     }'
```

## Project Structure

```
air-task1-backend-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database configuration and connection
│   ├── schemas.py           # Pydantic models for API request/response
│   ├── init_data.py         # Test data initialization
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py        # SQLAlchemy database models
│   └── routers/
│       ├── __init__.py
│       ├── customers.py     # Customer CRUD endpoints
│       ├── categories.py    # Category CRUD endpoints
│       ├── items.py         # Shop item CRUD endpoints
│       └── orders.py        # Order CRUD endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test configuration and fixtures
│   ├── test_customers.py    # Customer endpoint tests
│   ├── test_categories.py   # Category endpoint tests
│   ├── test_items.py        # Shop item endpoint tests
│   └── test_orders.py       # Order endpoint tests
├── requirements.txt         # Python dependencies
├── shop.db                  # SQLite database (created automatically)
└── README.md               # This file
```

## Database

The application uses SQLite as the database, which is automatically created as `shop.db` in the project root when you first run the application. The database schema is created automatically using SQLAlchemy's `create_all()` method.

## Dependencies

- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI applications
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library
- **Pydantic**: Data validation and settings management using Python type annotations
- **Pytest**: Testing framework
- **HTTPX**: HTTP client library for testing
- **Pytest-asyncio**: Pytest plugin for testing asyncio code