import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_customer(client):
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    customer_data = {
        "name": "Test",
        "surname": "Customer",
        "email": f"test.customer{unique_id}@example.com"
    }
    response = client.post("/customers/", json=customer_data)
    return response.json()

@pytest.fixture
def test_item(client):
    # Create category first
    category_data = {
        "title": "Test Category",
        "description": "Test category for orders"
    }
    category_response = client.post("/categories/", json=category_data)
    category = category_response.json()
    
    # Create item
    item_data = {
        "title": "Test Item",
        "description": "Test item for orders",
        "price": 99.99,
        "category_ids": [category["id"]]
    }
    response = client.post("/items/", json=item_data)
    return response.json()

@pytest.fixture
def test_order_data(test_customer, test_item):
    return {
        "customer_id": test_customer["id"],
        "items": [
            {
                "shop_item_id": test_item["id"],
                "quantity": 2
            }
        ]
    }

class TestOrders:
    def test_create_order(self, client, test_order_data):
        response = client.post("/orders/", json=test_order_data)
        assert response.status_code == 200
        data = response.json()
        assert data["customer_id"] == test_order_data["customer_id"]
        assert "id" in data
        assert len(data["items"]) == 1
        assert data["items"][0]["quantity"] == 2

    def test_create_order_customer_not_found(self, client, test_item):
        order_data = {
            "customer_id": 999,
            "items": [
                {
                    "shop_item_id": test_item["id"],
                    "quantity": 1
                }
            ]
        }
        response = client.post("/orders/", json=order_data)
        assert response.status_code == 404
        assert "Customer not found" in response.json()["detail"]

    def test_create_order_item_not_found(self, client, test_customer):
        order_data = {
            "customer_id": test_customer["id"],
            "items": [
                {
                    "shop_item_id": 999,
                    "quantity": 1
                }
            ]
        }
        response = client.post("/orders/", json=order_data)
        assert response.status_code == 404
        assert "Shop item with id 999 not found" in response.json()["detail"]

    def test_create_order_empty_items(self, client, test_customer):
        order_data = {
            "customer_id": test_customer["id"],
            "items": []
        }
        response = client.post("/orders/", json=order_data)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 0

    def test_read_orders(self, client, test_order_data):
        # Create an order first
        client.post("/orders/", json=test_order_data)
        
        response = client.get("/orders/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_read_order(self, client, test_order_data):
        # Create an order first
        create_response = client.post("/orders/", json=test_order_data)
        order_id = create_response.json()["id"]
        
        response = client.get(f"/orders/{order_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == order_id
        assert data["customer_id"] == test_order_data["customer_id"]

    def test_read_order_not_found(self, client):
        response = client.get("/orders/999")
        assert response.status_code == 404
        assert "Order not found" in response.json()["detail"]

    def test_update_order_customer(self, client, test_order_data, test_customer):
        # Create another customer
        customer_data = {
            "name": "Another",
            "surname": "Customer",
            "email": "another.customer@example.com"
        }
        customer_response = client.post("/customers/", json=customer_data)
        customer2_id = customer_response.json()["id"]
        
        # Create an order first
        create_response = client.post("/orders/", json=test_order_data)
        order_id = create_response.json()["id"]
        
        # Update order customer
        update_data = {"customer_id": customer2_id}
        response = client.put(f"/orders/{order_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["customer_id"] == customer2_id

    def test_update_order_items(self, client, test_order_data, test_item):
        # Create another item
        category_data = {
            "title": "Another Category",
            "description": "Another test category"
        }
        category_response = client.post("/categories/", json=category_data)
        category = category_response.json()
        
        item_data = {
            "title": "Another Item",
            "description": "Another test item",
            "price": 149.99,
            "category_ids": [category["id"]]
        }
        item_response = client.post("/items/", json=item_data)
        item2 = item_response.json()
        
        # Create an order first
        create_response = client.post("/orders/", json=test_order_data)
        order_id = create_response.json()["id"]
        
        # Update order items
        update_data = {
            "items": [
                {
                    "shop_item_id": test_item["id"],
                    "quantity": 1
                },
                {
                    "shop_item_id": item2["id"],
                    "quantity": 3
                }
            ]
        }
        response = client.put(f"/orders/{order_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2

    def test_update_order_not_found(self, client):
        update_data = {"customer_id": 1}
        response = client.put("/orders/999", json=update_data)
        assert response.status_code == 404
        assert "Order not found" in response.json()["detail"]

    def test_delete_order(self, client, test_order_data):
        # Create an order first
        create_response = client.post("/orders/", json=test_order_data)
        order_id = create_response.json()["id"]
        
        response = client.delete(f"/orders/{order_id}")
        assert response.status_code == 200
        
        # Verify order is deleted
        get_response = client.get(f"/orders/{order_id}")
        assert get_response.status_code == 404

    def test_delete_order_not_found(self, client):
        response = client.delete("/orders/999")
        assert response.status_code == 404
        assert "Order not found" in response.json()["detail"]
