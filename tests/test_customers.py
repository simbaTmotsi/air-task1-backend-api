import pytest
from fastapi.testclient import TestClient

def test_create_customer(client: TestClient):
    """Test creating a new customer"""
    customer_data = {
        "name": "John",
        "surname": "Doe",
        "email": "john.doe@example.com"
    }
    response = client.post("/customers/", json=customer_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John"
    assert data["surname"] == "Doe"
    assert data["email"] == "john.doe@example.com"
    assert "id" in data

def test_create_customer_duplicate_email(client: TestClient):
    """Test creating customer with duplicate email"""
    customer_data = {
        "name": "John",
        "surname": "Doe",
        "email": "john.doe@example.com"
    }
    # Create first customer
    response1 = client.post("/customers/", json=customer_data)
    assert response1.status_code == 200
    
    # Try to create second customer with same email
    response2 = client.post("/customers/", json=customer_data)
    assert response2.status_code == 400
    assert "Email already registered" in response2.json()["detail"]

def test_get_customers(client: TestClient):
    """Test getting all customers"""
    # Create test customers
    customers = [
        {"name": "John", "surname": "Doe", "email": "john.doe@example.com"},
        {"name": "Jane", "surname": "Smith", "email": "jane.smith@example.com"}
    ]
    
    for customer in customers:
        client.post("/customers/", json=customer)
    
    response = client.get("/customers/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_get_customer_by_id(client: TestClient):
    """Test getting a customer by ID"""
    customer_data = {
        "name": "John",
        "surname": "Doe",
        "email": "john.doe@example.com"
    }
    create_response = client.post("/customers/", json=customer_data)
    customer_id = create_response.json()["id"]
    
    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John"
    assert data["id"] == customer_id

def test_get_customer_not_found(client: TestClient):
    """Test getting a non-existent customer"""
    response = client.get("/customers/999")
    assert response.status_code == 404
    assert "Customer not found" in response.json()["detail"]

def test_update_customer(client: TestClient):
    """Test updating a customer"""
    customer_data = {
        "name": "John",
        "surname": "Doe",
        "email": "john.doe@example.com"
    }
    create_response = client.post("/customers/", json=customer_data)
    customer_id = create_response.json()["id"]
    
    update_data = {
        "name": "Johnny",
        "surname": "Smith"
    }
    response = client.put(f"/customers/{customer_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Johnny"
    assert data["surname"] == "Smith"
    assert data["email"] == "john.doe@example.com"  # Unchanged

def test_update_customer_not_found(client: TestClient):
    """Test updating a non-existent customer"""
    update_data = {"name": "Johnny"}
    response = client.put("/customers/999", json=update_data)
    assert response.status_code == 404
    assert "Customer not found" in response.json()["detail"]

def test_delete_customer(client: TestClient):
    """Test deleting a customer"""
    customer_data = {
        "name": "John",
        "surname": "Doe",
        "email": "john.doe@example.com"
    }
    create_response = client.post("/customers/", json=customer_data)
    customer_id = create_response.json()["id"]
    
    response = client.delete(f"/customers/{customer_id}")
    assert response.status_code == 200
    assert "Customer deleted successfully" in response.json()["message"]
    
    # Verify customer is deleted
    get_response = client.get(f"/customers/{customer_id}")
    assert get_response.status_code == 404

def test_delete_customer_not_found(client: TestClient):
    """Test deleting a non-existent customer"""
    response = client.delete("/customers/999")
    assert response.status_code == 404
    assert "Customer not found" in response.json()["detail"]