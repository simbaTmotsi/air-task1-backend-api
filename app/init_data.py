from app.database import SessionLocal
from app.models.models import Customer, ShopItemCategory, ShopItem, Order, OrderItem

def create_test_data():
    """Create initial test data for the application"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Customer).first():
            return  # Data already exists
        
        # Create test customers
        customers = [
            Customer(name="John", surname="Doe", email="john.doe@example.com"),
            Customer(name="Jane", surname="Smith", email="jane.smith@example.com"),
            Customer(name="Bob", surname="Johnson", email="bob.johnson@example.com")
        ]
        
        for customer in customers:
            db.add(customer)
        
        # Create test categories
        categories = [
            ShopItemCategory(title="Electronics", description="Electronic devices and gadgets"),
            ShopItemCategory(title="Books", description="Books of various genres"),
            ShopItemCategory(title="Clothing", description="Apparel and accessories"),
            ShopItemCategory(title="Home & Garden", description="Home improvement and garden items")
        ]
        
        for category in categories:
            db.add(category)
        
        db.commit()  # Commit to get IDs
        
        # Create test items
        items = [
            ShopItem(title="Smartphone", description="Latest model smartphone", price=599.99),
            ShopItem(title="Laptop", description="High-performance laptop", price=1299.99),
            ShopItem(title="Python Programming Book", description="Learn Python programming", price=39.99),
            ShopItem(title="T-Shirt", description="Comfortable cotton t-shirt", price=19.99),
            ShopItem(title="Garden Hose", description="50ft garden hose", price=29.99)
        ]
        
        # Add items and assign categories
        items[0].categories = [categories[0]]  # Smartphone -> Electronics
        items[1].categories = [categories[0]]  # Laptop -> Electronics
        items[2].categories = [categories[1]]  # Book -> Books
        items[3].categories = [categories[2]]  # T-Shirt -> Clothing
        items[4].categories = [categories[3]]  # Garden Hose -> Home & Garden
        
        for item in items:
            db.add(item)
        
        db.commit()  # Commit to get IDs
        
        # Create test orders
        orders = [
            Order(customer_id=customers[0].id),
            Order(customer_id=customers[1].id)
        ]
        
        for order in orders:
            db.add(order)
        
        db.commit()  # Commit to get order IDs
        
        # Create test order items
        order_items = [
            OrderItem(shop_item_id=items[0].id, quantity=1, order_id=orders[0].id),  # John orders 1 Smartphone
            OrderItem(shop_item_id=items[2].id, quantity=2, order_id=orders[0].id),  # John orders 2 Books
            OrderItem(shop_item_id=items[1].id, quantity=1, order_id=orders[1].id),  # Jane orders 1 Laptop
            OrderItem(shop_item_id=items[3].id, quantity=3, order_id=orders[1].id)   # Jane orders 3 T-Shirts
        ]
        
        for order_item in order_items:
            db.add(order_item)
        
        db.commit()
        print("Test data created successfully!")
        
    except Exception as e:
        print(f"Error creating test data: {e}")
        db.rollback()
    finally:
        db.close()