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
def test_category(client):
    category_data = {
        "title": "Test Category",
        "description": "Test category for items"
    }
    response = client.post("/categories/", json=category_data)
    return response.json()

@pytest.fixture
def test_item_data(test_category):
    return {
        "title": "Test Item",
        "description": "Test item description",
        "price": 99.99,
        "category_ids": [test_category["id"]]
    }

class TestItems:
    def test_create_item(self, client, test_item_data):
        response = client.post("/items/", json=test_item_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == test_item_data["title"]
        assert data["description"] == test_item_data["description"]
        assert data["price"] == test_item_data["price"]
        assert "id" in data
        assert len(data["categories"]) == 1

    def test_create_item_without_categories(self, client):
        item_data = {
            "title": "Test Item No Category",
            "description": "Test item without categories",
            "price": 49.99,
            "category_ids": []
        }
        response = client.post("/items/", json=item_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == item_data["title"]
        assert len(data["categories"]) == 0

    def test_read_items(self, client, test_item_data):
        # Create an item first
        client.post("/items/", json=test_item_data)
        
        response = client.get("/items/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_read_item(self, client, test_item_data):
        # Create an item first
        create_response = client.post("/items/", json=test_item_data)
        item_id = create_response.json()["id"]
        
        response = client.get(f"/items/{item_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == item_id
        assert data["title"] == test_item_data["title"]

    def test_read_item_not_found(self, client):
        response = client.get("/items/999")
        assert response.status_code == 404
        assert "Shop item not found" in response.json()["detail"]

    def test_update_item(self, client, test_item_data):
        # Create an item first
        create_response = client.post("/items/", json=test_item_data)
        item_id = create_response.json()["id"]
        
        update_data = {"title": "Updated Item", "price": 149.99}
        response = client.put(f"/items/{item_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Item"
        assert data["price"] == 149.99
        assert data["description"] == test_item_data["description"]

    def test_update_item_categories(self, client, test_item_data, test_category):
        # Create another category
        category_data = {
            "title": "Another Category",
            "description": "Another test category"
        }
        category_response = client.post("/categories/", json=category_data)
        category2_id = category_response.json()["id"]
        
        # Create an item first
        create_response = client.post("/items/", json=test_item_data)
        item_id = create_response.json()["id"]
        
        # Update with multiple categories
        update_data = {"category_ids": [test_category["id"], category2_id]}
        response = client.put(f"/items/{item_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert len(data["categories"]) == 2

    def test_update_item_not_found(self, client):
        update_data = {"title": "Updated Item"}
        response = client.put("/items/999", json=update_data)
        assert response.status_code == 404
        assert "Shop item not found" in response.json()["detail"]

    def test_delete_item(self, client, test_item_data):
        # Create an item first
        create_response = client.post("/items/", json=test_item_data)
        item_id = create_response.json()["id"]
        
        response = client.delete(f"/items/{item_id}")
        assert response.status_code == 200
        
        # Verify item is deleted
        get_response = client.get(f"/items/{item_id}")
        assert get_response.status_code == 404

    def test_delete_item_not_found(self, client):
        response = client.delete("/items/999")
        assert response.status_code == 404
        assert "Shop item not found" in response.json()["detail"]
