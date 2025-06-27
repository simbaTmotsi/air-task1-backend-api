import pytest
from fastapi.testclient import TestClient

def test_create_item_without_categories(client: TestClient):
    """Test creating a new item without categories"""
    item_data = {
        "title": "Smartphone",
        "description": "Latest model smartphone",
        "price": 599.99,
        "category_ids": []
    }
    response = client.post("/items/", json=item_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Smartphone"
    assert data["description"] == "Latest model smartphone"
    assert data["price"] == 599.99
    assert data["categories"] == []
    assert "id" in data

def test_create_item_with_categories(client: TestClient):
    """Test creating a new item with categories"""
    # First create a category
    category_data = {
        "title": "Electronics",
        "description": "Electronic devices"
    }
    category_response = client.post("/categories/", json=category_data)
    category_id = category_response.json()["id"]
    
    # Then create an item with that category
    item_data = {
        "title": "Smartphone",
        "description": "Latest model smartphone",
        "price": 599.99,
        "category_ids": [category_id]
    }
    response = client.post("/items/", json=item_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Smartphone"
    assert len(data["categories"]) == 1
    assert data["categories"][0]["title"] == "Electronics"

def test_create_item_with_invalid_category(client: TestClient):
    """Test creating item with non-existent category"""
    item_data = {
        "title": "Smartphone",
        "description": "Latest model smartphone",
        "price": 599.99,
        "category_ids": [999]  # Non-existent category
    }
    response = client.post("/items/", json=item_data)
    assert response.status_code == 400
    assert "One or more categories not found" in response.json()["detail"]

def test_get_items(client: TestClient):
    """Test getting all items"""
    items = [
        {"title": "Smartphone", "description": "Latest smartphone", "price": 599.99, "category_ids": []},
        {"title": "Laptop", "description": "High-performance laptop", "price": 1299.99, "category_ids": []}
    ]
    
    for item in items:
        client.post("/items/", json=item)
    
    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_get_item_by_id(client: TestClient):
    """Test getting an item by ID"""
    item_data = {
        "title": "Smartphone",
        "description": "Latest model smartphone",
        "price": 599.99,
        "category_ids": []
    }
    create_response = client.post("/items/", json=item_data)
    item_id = create_response.json()["id"]
    
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Smartphone"
    assert data["id"] == item_id

def test_get_item_not_found(client: TestClient):
    """Test getting a non-existent item"""
    response = client.get("/items/999")
    assert response.status_code == 404
    assert "Item not found" in response.json()["detail"]

def test_update_item(client: TestClient):
    """Test updating an item"""
    item_data = {
        "title": "Smartphone",
        "description": "Latest model smartphone",
        "price": 599.99,
        "category_ids": []
    }
    create_response = client.post("/items/", json=item_data)
    item_id = create_response.json()["id"]
    
    update_data = {
        "title": "Premium Smartphone",
        "price": 699.99
    }
    response = client.put(f"/items/{item_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Premium Smartphone"
    assert data["price"] == 699.99
    assert data["description"] == "Latest model smartphone"  # Unchanged

def test_update_item_categories(client: TestClient):
    """Test updating item categories"""
    # Create categories
    category1_data = {"title": "Electronics", "description": "Electronic devices"}
    category2_data = {"title": "Mobile", "description": "Mobile devices"}
    
    category1_response = client.post("/categories/", json=category1_data)
    category2_response = client.post("/categories/", json=category2_data)
    
    category1_id = category1_response.json()["id"]
    category2_id = category2_response.json()["id"]
    
    # Create item
    item_data = {
        "title": "Smartphone",
        "description": "Latest model smartphone",
        "price": 599.99,
        "category_ids": [category1_id]
    }
    create_response = client.post("/items/", json=item_data)
    item_id = create_response.json()["id"]
    
    # Update categories
    update_data = {
        "category_ids": [category1_id, category2_id]
    }
    response = client.put(f"/items/{item_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert len(data["categories"]) == 2

def test_update_item_not_found(client: TestClient):
    """Test updating a non-existent item"""
    update_data = {"title": "New Title"}
    response = client.put("/items/999", json=update_data)
    assert response.status_code == 404
    assert "Item not found" in response.json()["detail"]

def test_delete_item(client: TestClient):
    """Test deleting an item"""
    item_data = {
        "title": "Smartphone",
        "description": "Latest model smartphone",
        "price": 599.99,
        "category_ids": []
    }
    create_response = client.post("/items/", json=item_data)
    item_id = create_response.json()["id"]
    
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200
    assert "Item deleted successfully" in response.json()["message"]
    
    # Verify item is deleted
    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404

def test_delete_item_not_found(client: TestClient):
    """Test deleting a non-existent item"""
    response = client.delete("/items/999")
    assert response.status_code == 404
    assert "Item not found" in response.json()["detail"]