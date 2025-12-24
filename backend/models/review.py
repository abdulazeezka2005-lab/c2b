from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

class ReviewCreate(BaseModel):
    productId: str
    customerName: str
    customerEmail: str
    rating: int  # 1-5
    comment: str

class Review(BaseModel):
    id: str = Field(alias="_id")
    productId: str
    customerName: str
    customerEmail: str
    rating: int
    comment: str
    approved: bool = False
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
