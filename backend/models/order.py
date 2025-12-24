from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from bson import ObjectId

class OrderItem(BaseModel):
    productId: str
    productName: str
    price: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItem]
    customerPhone: str

class Order(BaseModel):
    id: str = Field(alias="_id")
    items: List[OrderItem]
    totalAmount: int
    customerPhone: str
    status: str = "pending"
    orderDate: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
