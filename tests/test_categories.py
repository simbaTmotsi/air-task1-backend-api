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
def test_category_data():
    return {
        "title": "Test Category",
        "description": "Test category description"
    }

class TestCategories:
    def test_create_category(self, client, test_category_data):
        response = client.post("/categories/", json=test_category_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == test_category_data["title"]
        assert data["description"] == test_category_data["description"]
        assert "id" in data

    def test_read_categories(self, client, test_category_data):
        # Create a category first
        client.post("/categories/", json=test_category_data)
        
        response = client.get("/categories/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_read_category(self, client, test_category_data):
        # Create a category first
        create_response = client.post("/categories/", json=test_category_data)
        category_id = create_response.json()["id"]
        
        response = client.get(f"/categories/{category_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == category_id
        assert data["title"] == test_category_data["title"]

    def test_read_category_not_found(self, client):
        response = client.get("/categories/999")
        assert response.status_code == 404
        assert "Category not found" in response.json()["detail"]

    def test_update_category(self, client, test_category_data):
        # Create a category first
        create_response = client.post("/categories/", json=test_category_data)
        category_id = create_response.json()["id"]
        
        update_data = {"title": "Updated Category"}
        response = client.put(f"/categories/{category_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Category"
        assert data["description"] == test_category_data["description"]

    def test_update_category_not_found(self, client):
        update_data = {"title": "Updated Category"}
        response = client.put("/categories/999", json=update_data)
        assert response.status_code == 404
        assert "Category not found" in response.json()["detail"]

    def test_delete_category(self, client, test_category_data):
        # Create a category first
        create_response = client.post("/categories/", json=test_category_data)
        category_id = create_response.json()["id"]
        
        response = client.delete(f"/categories/{category_id}")
        assert response.status_code == 200
        
        # Verify category is deleted
        get_response = client.get(f"/categories/{category_id}")
        assert get_response.status_code == 404

    def test_delete_category_not_found(self, client):
        response = client.delete("/categories/999")
        assert response.status_code == 404
        assert "Category not found" in response.json()["detail"]
