from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional

# Customer Schemas
class CustomerBase(BaseModel):
    name: str
    surname: str
    email: str

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None

class Customer(CustomerBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# ShopItemCategory Schemas
class ShopItemCategoryBase(BaseModel):
    title: str
    description: str

class ShopItemCategoryCreate(ShopItemCategoryBase):
    pass

class ShopItemCategoryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class ShopItemCategory(ShopItemCategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# ShopItem Schemas
class ShopItemBase(BaseModel):
    title: str
    description: str
    price: float

class ShopItemCreate(ShopItemBase):
    category_ids: List[int] = []

class ShopItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_ids: Optional[List[int]] = None

class ShopItem(ShopItemBase):
    id: int
    categories: List[ShopItemCategory] = []
    model_config = ConfigDict(from_attributes=True)

# OrderItem Schemas
class OrderItemBase(BaseModel):
    shop_item_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(BaseModel):
    shop_item_id: Optional[int] = None
    quantity: Optional[int] = None

class OrderItem(OrderItemBase):
    id: int
    shop_item: ShopItem
    model_config = ConfigDict(from_attributes=True)

# Order Schemas
class OrderBase(BaseModel):
    customer_id: int

class OrderCreate(OrderBase):
    items: List[OrderItemCreate] = []

class OrderUpdate(BaseModel):
    customer_id: Optional[int] = None
    items: Optional[List[OrderItemCreate]] = None

class Order(OrderBase):
    id: int
    customer: Customer
    items: List[OrderItem] = []
    model_config = ConfigDict(from_attributes=True)
