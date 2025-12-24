from fastapi import APIRouter, HTTPException, Depends, Header
from models.admin import AdminLogin, AdminToken
from datetime import datetime, timedelta
import os
import jwt
import bcrypt
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter(prefix="/admin", tags=["admin"])

SECRET_KEY = os.environ.get('JWT_SECRET', 'your-secret-key-change-in-production')

def get_database():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    return client[os.environ['DB_NAME']]

def create_token(username: str) -> str:
    expiration = datetime.utcnow() + timedelta(days=7)
    token = jwt.encode(
        {"username": username, "exp": expiration},
        SECRET_KEY,
        algorithm="HS256"
    )
    return token

def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = authorization.replace('Bearer ', '')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["username"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/login", response_model=dict)
async def admin_login(credentials: AdminLogin):
    try:
        db = get_database()
        
        # Find admin
        admin = await db.admins.find_one({"username": credentials.username})
        
        if not admin:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Verify password
        if not bcrypt.checkpw(credentials.password.encode('utf-8'), admin['passwordHash'].encode('utf-8')):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Create token
        token = create_token(credentials.username)
        
        return {
            "token": token,
            "username": credentials.username,
            "message": "Login successful"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create-admin", response_model=dict)
async def create_admin_user():
    """One-time endpoint to create admin user"""
    try:
        db = get_database()
        
        # Check if admin already exists
        existing_admin = await db.admins.find_one({"username": "admin"})
        if existing_admin:
            return {"message": "Admin already exists"}
        
        # Create admin with default password
        password_hash = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
        
        admin = {
            "username": "admin",
            "passwordHash": password_hash.decode('utf-8'),
            "createdAt": datetime.utcnow()
        }
        
        result = await db.admins.insert_one(admin)
        
        return {
            "message": "Admin created successfully",
            "username": "admin",
            "defaultPassword": "admin123",
            "note": "Please change the password after first login"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/verify", response_model=dict)
async def verify_admin_token(username: str = Depends(verify_token)):
    return {"valid": True, "username": username}
