from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class PaymentOrderCreate(BaseModel):
    amount: int  # in paise
    currency: str = "INR"
    orderId: str  # our order ID

class PaymentVerification(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str

class Payment(BaseModel):
    id: str = Field(alias="_id")
    orderId: str
    razorpayOrderId: str
    razorpayPaymentId: Optional[str] = None
    amount: int
    currency: str
    status: str  # created, paid, failed
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    paidAt: Optional[datetime] = None

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
