from fastapi import APIRouter, HTTPException, Request
from models.payment import PaymentOrderCreate, PaymentVerification
from datetime import datetime
import os
from dotenv import load_dotenv
from pathlib import Path
import razorpay
import hmac
import hashlib
from motor.motor_asyncio import AsyncIOMotorClient

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

router = APIRouter(prefix="/payments", tags=["payments"])

def get_database():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    return client[os.environ['DB_NAME']]

# Initialize Razorpay client with live keys
RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID', 'test_key')
RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', 'test_secret')

print(f"Razorpay initialized with Key ID: {RAZORPAY_KEY_ID[:15]}...")

try:
    razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
except Exception as e:
    print(f"Razorpay client initialization warning: {e}")
    razorpay_client = None

@router.get("/config", response_model=dict)
async def get_razorpay_config():
    """Get Razorpay public key for frontend"""
    return {"key": RAZORPAY_KEY_ID}

@router.post("/create-order", response_model=dict)
async def create_payment_order(payment_order: PaymentOrderCreate):
    try:
        db = get_database()
        
        if not razorpay_client:
            raise HTTPException(status_code=500, detail="Razorpay not configured")
        
        # Create Razorpay order
        razorpay_order = razorpay_client.order.create({
            "amount": payment_order.amount,
            "currency": payment_order.currency,
            "payment_capture": 1
        })
        
        # Save to database
        payment = {
            "orderId": payment_order.orderId,
            "razorpayOrderId": razorpay_order["id"],
            "amount": payment_order.amount,
            "currency": payment_order.currency,
            "status": "created",
            "createdAt": datetime.utcnow()
        }
        
        result = await db.payments.insert_one(payment)
        payment["_id"] = str(result.inserted_id)
        
        return {
            "orderId": razorpay_order["id"],
            "amount": razorpay_order["amount"],
            "currency": razorpay_order["currency"],
            "key": RAZORPAY_KEY_ID
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/verify", response_model=dict)
async def verify_payment(verification: PaymentVerification):
    try:
        db = get_database()
        
        # Verify signature
        generated_signature = hmac.new(
            RAZORPAY_KEY_SECRET.encode('utf-8'),
            f"{verification.razorpay_order_id}|{verification.razorpay_payment_id}".encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        if generated_signature != verification.razorpay_signature:
            raise HTTPException(status_code=400, detail="Invalid signature")
        
        # Update payment status
        result = await db.payments.update_one(
            {"razorpayOrderId": verification.razorpay_order_id},
            {
                "$set": {
                    "razorpayPaymentId": verification.razorpay_payment_id,
                    "status": "paid",
                    "paidAt": datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        # Update order status to paid
        payment = await db.payments.find_one({"razorpayOrderId": verification.razorpay_order_id})
        if payment:
            await db.orders.update_one(
                {"_id": payment["orderId"]},
                {"$set": {"paymentStatus": "paid"}}
            )
        
        return {"status": "success", "message": "Payment verified successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhook")
async def razorpay_webhook(request: Request):
    """Handle Razorpay webhooks"""
    try:
        payload = await request.body()
        signature = request.headers.get('X-Razorpay-Signature', '')
        
        # Verify webhook signature (if webhook secret is configured)
        webhook_secret = os.environ.get('RAZORPAY_WEBHOOK_SECRET')
        if webhook_secret:
            expected_signature = hmac.new(
                webhook_secret.encode('utf-8'),
                payload,
                hashlib.sha256
            ).hexdigest()
            
            if signature != expected_signature:
                raise HTTPException(status_code=400, detail="Invalid webhook signature")
        
        # Process webhook event
        return {"status": "processed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
