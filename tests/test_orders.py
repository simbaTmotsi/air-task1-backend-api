import pytest
from fastapi.testclient import TestClient

def test_create_order_empty(client: TestClient):
    """Test creating an order with no items"""
    # First create a customer
    customer_data = {"name": "John", "surname": "Doe", "email": "john.doe@example.com"}
    customer_response = client.post("/customers/", json=customer_data)
    customer_id = customer_response.json()["id"]
    
    order_data = {
        "customer_id": customer_id,
        "items": []
    }
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == customer_id
    assert data["items"] == []
    assert "id" in data

def test_create_order_with_items(client: TestClient):
    """Test creating an order with items"""
    # Create customer
    customer_data = {"name": "John", "surname": "Doe", "email": "john.doe@example.com"}
    customer_response = client.post("/customers/", json=customer_data)
    customer_id = customer_response.json()["id"]
    
    # Create item
    item_data = {"title": "Smartphone", "description": "Latest smartphone", "price": 599.99, "category_ids": []}
    item_response = client.post("/items/", json=item_data)
    item_id = item_response.json()["id"]
    
    # Create order with items
    order_data = {
        "customer_id": customer_id,
        "items": [
            {"shop_item_id": item_id, "quantity": 2}
        ]
    }
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == customer_id
    assert len(data["items"]) == 1
    assert data["items"][0]["quantity"] == 2
    assert data["items"][0]["shop_item"]["id"] == item_id

def test_create_order_invalid_customer(client: TestClient):
    """Test creating order with non-existent customer"""
    order_data = {
        "customer_id": 999,  # Non-existent customer
        "items": []
    }
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 400
    assert "Customer not found" in response.json()["detail"]

def test_create_order_invalid_item(client: TestClient):
    """Test creating order with non-existent item"""
    # Create customer
    customer_data = {"name": "John", "surname": "Doe", "email": "john.doe@example.com"}
    customer_response = client.post("/customers/", json=customer_data)
    customer_id = customer_response.json()["id"]
    
    order_data = {
        "customer_id": customer_id,
        "items": [
            {"shop_item_id": 999, "quantity": 1}  # Non-existent item
        ]
    }
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 400
    assert "Shop item with ID 999 not found" in response.json()["detail"]

def test_get_orders(client: TestClient):
    """Test getting all orders"""
    # Create customer
    customer_data = {"name": "John", "surname": "Doe", "email": "john.doe@example.com"}
    customer_response = client.post("/customers/", json=customer_data)
    customer_id = customer_response.json()["id"]
    
    # Create orders
    orders = [
        {"customer_id": customer_id, "items": []},
        {"customer_id": customer_id, "items": []}
    ]
    
    for order in orders:
        client.post("/orders/", json=order)
    
    response = client.get("/orders/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_get_order_by_id(client: TestClient):
    """Test getting an order by ID"""
    # Create customer
    customer_data = {"name": "John", "surname": "Doe", "email": "john.doe@example.com"}
    customer_response = client.post("/customers/", json=customer_data)
    customer_id = customer_response.json()["id"]
    
    order_data = {"customer_id": customer_id, "items": []}
    create_response = client.post("/orders/", json=order_data)
    order_id = create_response.json()["id"]
    
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == customer_id
    assert data["id"] == order_id

def test_get_order_not_found(client: TestClient):
    """Test getting a non-existent order"""
    response = client.get("/orders/999")
    assert response.status_code == 404
    assert "Order not found" in response.json()["detail"]

def test_update_order_customer(client: TestClient):
    """Test updating order customer"""
    # Create customers
    customer1_data = {"name": "John", "surname": "Doe", "email": "john.doe@example.com"}
    customer2_data = {"name": "Jane", "surname": "Smith", "email": "jane.smith@example.com"}
    
    customer1_response = client.post("/customers/", json=customer1_data)
    customer2_response = client.post("/customers/", json=customer2_data)
    
    customer1_id = customer1_response.json()["id"]
    customer2_id = customer2_response.json()["id"]
    
    # Create order
    order_data = {"customer_id": customer1_id, "items": []}
    create_response = client.post("/orders/", json=order_data)
    order_id = create_response.json()["id"]
    
    # Update order customer
    update_data = {"customer_id": customer2_id}
    response = client.put(f"/orders/{order_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == customer2_id

def test_update_order_items(client: TestClient):
    """Test updating order items"""
    # Create customer and items
    customer_data = {"name": "John", "surname": "Doe", "email": "john.doe@example.com"}
    customer_response = client.post("/customers/", json=customer_data)
    customer_id = customer_response.json()["id"]
    
    item1_data = {"title": "Smartphone", "description": "Latest smartphone", "price": 599.99, "category_ids": []}
    item2_data = {"title": "Laptop", "description": "High-performance laptop", "price": 1299.99, "category_ids": []}
    
    item1_response = client.post("/items/", json=item1_data)
    item2_response = client.post("/items/", json=item2_data)
    
    item1_id = item1_response.json()["id"]
    item2_id = item2_response.json()["id"]
    
    # Create order with one item
    order_data = {
        "customer_id": customer_id,
        "items": [{"shop_item_id": item1_id, "quantity": 1}]
    }
    create_response = client.post("/orders/", json=order_data)
    order_id = create_response.json()["id"]
    
    # Update order items
    update_data = {
        "items": [
            {"shop_item_id": item1_id, "quantity": 2},
            {"shop_item_id": item2_id, "quantity": 1}
        ]
    }
    response = client.put(f"/orders/{order_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    
    # Check quantities
    quantities = {item["shop_item"]["id"]: item["quantity"] for item in data["items"]}
    assert quantities[item1_id] == 2
    assert quantities[item2_id] == 1

def test_update_order_not_found(client: TestClient):
    """Test updating a non-existent order"""
    update_data = {"customer_id": 1}
    response = client.put("/orders/999", json=update_data)
    assert response.status_code == 404
    assert "Order not found" in response.json()["detail"]

def test_delete_order(client: TestClient):
    """Test deleting an order"""
    # Create customer
    customer_data = {"name": "John", "surname": "Doe", "email": "john.doe@example.com"}
    customer_response = client.post("/customers/", json=customer_data)
    customer_id = customer_response.json()["id"]
    
    order_data = {"customer_id": customer_id, "items": []}
    create_response = client.post("/orders/", json=order_data)
    order_id = create_response.json()["id"]
    
    response = client.delete(f"/orders/{order_id}")
    assert response.status_code == 200
    assert "Order deleted successfully" in response.json()["message"]
    
    # Verify order is deleted
    get_response = client.get(f"/orders/{order_id}")
    assert get_response.status_code == 404

def test_delete_order_not_found(client: TestClient):
    """Test deleting a non-existent order"""
    response = client.delete("/orders/999")
    assert response.status_code == 404
    assert "Order not found" in response.json()["detail"]