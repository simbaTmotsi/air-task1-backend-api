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
def test_customer_data():
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    return {
        "name": "Test",
        "surname": "Customer",
        "email": f"test{unique_id}@example.com"
    }

class TestCustomers:
    def test_create_customer(self, client, test_customer_data):
        response = client.post("/customers/", json=test_customer_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == test_customer_data["name"]
        assert data["surname"] == test_customer_data["surname"]
        assert data["email"] == test_customer_data["email"]
        assert "id" in data

    def test_create_customer_duplicate_email(self, client, test_customer_data):
        # First creation should succeed
        client.post("/customers/", json=test_customer_data)
        
        # Second creation with same email should fail
        response = client.post("/customers/", json=test_customer_data)
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_read_customers(self, client, test_customer_data):
        # Create a customer first
        client.post("/customers/", json=test_customer_data)
        
        response = client.get("/customers/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_read_customer(self, client, test_customer_data):
        # Create a customer first
        create_response = client.post("/customers/", json=test_customer_data)
        customer_id = create_response.json()["id"]
        
        response = client.get(f"/customers/{customer_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == customer_id
        assert data["name"] == test_customer_data["name"]

    def test_read_customer_not_found(self, client):
        response = client.get("/customers/999")
        assert response.status_code == 404
        assert "Customer not found" in response.json()["detail"]

    def test_update_customer(self, client, test_customer_data):
        # Create a customer first
        create_response = client.post("/customers/", json=test_customer_data)
        customer_id = create_response.json()["id"]
        
        update_data = {"name": "Updated Name"}
        response = client.put(f"/customers/{customer_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["surname"] == test_customer_data["surname"]

    def test_update_customer_not_found(self, client):
        update_data = {"name": "Updated Name"}
        response = client.put("/customers/999", json=update_data)
        assert response.status_code == 404
        assert "Customer not found" in response.json()["detail"]

    def test_delete_customer(self, client, test_customer_data):
        # Create a customer first
        create_response = client.post("/customers/", json=test_customer_data)
        customer_id = create_response.json()["id"]
        
        response = client.delete(f"/customers/{customer_id}")
        assert response.status_code == 200
        
        # Verify customer is deleted
        get_response = client.get(f"/customers/{customer_id}")
        assert get_response.status_code == 404

    def test_delete_customer_not_found(self, client):
        response = client.delete("/customers/999")
        assert response.status_code == 404
        assert "Customer not found" in response.json()["detail"]
