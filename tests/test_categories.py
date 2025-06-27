import pytest
from fastapi.testclient import TestClient

def test_create_category(client: TestClient):
    """Test creating a new category"""
    category_data = {
        "title": "Electronics",
        "description": "Electronic devices and gadgets"
    }
    response = client.post("/categories/", json=category_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Electronics"
    assert data["description"] == "Electronic devices and gadgets"
    assert "id" in data

def test_get_categories(client: TestClient):
    """Test getting all categories"""
    categories = [
        {"title": "Electronics", "description": "Electronic devices"},
        {"title": "Books", "description": "Books of various genres"}
    ]
    
    for category in categories:
        client.post("/categories/", json=category)
    
    response = client.get("/categories/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_get_category_by_id(client: TestClient):
    """Test getting a category by ID"""
    category_data = {
        "title": "Electronics",
        "description": "Electronic devices and gadgets"
    }
    create_response = client.post("/categories/", json=category_data)
    category_id = create_response.json()["id"]
    
    response = client.get(f"/categories/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Electronics"
    assert data["id"] == category_id

def test_get_category_not_found(client: TestClient):
    """Test getting a non-existent category"""
    response = client.get("/categories/999")
    assert response.status_code == 404
    assert "Category not found" in response.json()["detail"]

def test_update_category(client: TestClient):
    """Test updating a category"""
    category_data = {
        "title": "Electronics",
        "description": "Electronic devices and gadgets"
    }
    create_response = client.post("/categories/", json=category_data)
    category_id = create_response.json()["id"]
    
    update_data = {
        "title": "Consumer Electronics",
        "description": "Consumer electronic devices"
    }
    response = client.put(f"/categories/{category_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Consumer Electronics"
    assert data["description"] == "Consumer electronic devices"

def test_update_category_not_found(client: TestClient):
    """Test updating a non-existent category"""
    update_data = {"title": "New Title"}
    response = client.put("/categories/999", json=update_data)
    assert response.status_code == 404
    assert "Category not found" in response.json()["detail"]

def test_delete_category(client: TestClient):
    """Test deleting a category"""
    category_data = {
        "title": "Electronics",
        "description": "Electronic devices and gadgets"
    }
    create_response = client.post("/categories/", json=category_data)
    category_id = create_response.json()["id"]
    
    response = client.delete(f"/categories/{category_id}")
    assert response.status_code == 200
    assert "Category deleted successfully" in response.json()["message"]
    
    # Verify category is deleted
    get_response = client.get(f"/categories/{category_id}")
    assert get_response.status_code == 404

def test_delete_category_not_found(client: TestClient):
    """Test deleting a non-existent category"""
    response = client.delete("/categories/999")
    assert response.status_code == 404
    assert "Category not found" in response.json()["detail"]