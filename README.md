# Online Shop Backend API

A minimalistic backend web application for an online shop built with FastAPI and SQLAlchemy.

## Features

- Full CRUD operations for:
  - Customers
  - Shop Item Categories
  - Shop Items
  - Orders
- SQLite database with test data initialization
- Comprehensive API tests
- RESTful API design

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── crud.py              # CRUD operations
│   └── routers/             # API route handlers
│       ├── __init__.py
│       ├── customers.py
│       ├── categories.py
│       ├── items.py
│       └── orders.py
├── tests/
│   ├── __init__.py
│   ├── test_customers.py
│   ├── test_categories.py
│   ├── test_items.py
│   └── test_orders.py
├── requirements.txt
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd air-task1-backend-api
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the development server:
```bash
uvicorn app.main:app --reload
```

2. The API will be available at: `http://localhost:8000`

3. Access the interactive API documentation at: `http://localhost:8000/docs`

## API Endpoints

### Customers
- `GET /customers/` - List all customers
- `GET /customers/{customer_id}` - Get customer by ID
- `POST /customers/` - Create new customer
- `PUT /customers/{customer_id}` - Update customer
- `DELETE /customers/{customer_id}` - Delete customer

### Shop Item Categories
- `GET /categories/` - List all categories
- `GET /categories/{category_id}` - Get category by ID
- `POST /categories/` - Create new category
- `PUT /categories/{category_id}` - Update category
- `DELETE /categories/{category_id}` - Delete category

### Shop Items
- `GET /items/` - List all items
- `GET /items/{item_id}` - Get item by ID
- `POST /items/` - Create new item
- `PUT /items/{item_id}` - Update item
- `DELETE /items/{item_id}` - Delete item

### Orders
- `GET /orders/` - List all orders
- `GET /orders/{order_id}` - Get order by ID
- `POST /orders/` - Create new order
- `PUT /orders/{order_id}` - Update order
- `DELETE /orders/{order_id}` - Delete order

## Running Tests

Run all tests:
```bash
pytest
```

Run tests with verbose output:
```bash
pytest -v
```

Run specific test file:
```bash
pytest tests/test_customers.py
```

## Database

The application uses SQLite as the database. The database file (`shop.db`) will be created automatically when you first run the application. Test data is automatically seeded on startup.

## Development

The application includes:
- Automatic database table creation
- Test data initialization
- Comprehensive error handling
- Input validation using Pydantic
- Interactive API documentation
- Complete test coverage

## Technologies Used

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation using Python type annotations
- **SQLite** - Lightweight database engine
- **Pytest** - Testing framework
- **Uvicorn** - ASGI server
