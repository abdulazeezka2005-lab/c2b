from fastapi import APIRouter, HTTPException
from models.order import Order, OrderCreate
from datetime import datetime
import os
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter(prefix="/orders", tags=["orders"])

def get_database():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    return client[os.environ['DB_NAME']]

@router.post("", response_model=dict)
async def create_order(order: OrderCreate):
    try:
        db = get_database()
        # Calculate total amount
        total_amount = sum(item.price * item.quantity for item in order.items)
        
        order_dict = order.dict()
        order_dict["totalAmount"] = total_amount
        order_dict["status"] = "pending"
        order_dict["orderDate"] = datetime.utcnow()
        
        result = await db.orders.insert_one(order_dict)
        order_dict["_id"] = str(result.inserted_id)
        
        return {"order": order_dict, "message": "Order created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=dict)
async def get_orders():
    try:
        db = get_database()
        orders = await db.orders.find().sort("orderDate", -1).to_list(1000)
        
        # Convert ObjectId to string
        for order in orders:
            order["_id"] = str(order["_id"])
        
        return {"orders": orders, "count": len(orders)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
