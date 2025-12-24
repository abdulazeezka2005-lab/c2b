from fastapi import APIRouter, HTTPException
from datetime import datetime
import os
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter(prefix="/seed", tags=["seed"])

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

@router.post("", response_model=dict)
async def seed_database():
    try:
        # Check if already seeded
        existing_products = await db.products.count_documents({})
        if existing_products > 0:
            return {"message": "Database already seeded", "skipped": True}
        
        # Seed Products
        products = [
            {
                "name": "Luxury Gold Watch",
                "category": "watches",
                "price": 2999,
                "image": "https://images.unsplash.com/photo-1587836374852-dca8da20fd8d?w=800&h=800&fit=crop",
                "description": "Premium gold-plated watch with leather strap",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Sport Chronograph",
                "category": "watches",
                "price": 3499,
                "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&h=800&fit=crop",
                "description": "Water-resistant sports watch with chronograph",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Classic Silver Watch",
                "category": "watches",
                "price": 1999,
                "image": "https://images.unsplash.com/photo-1594534475808-b18fc33b045e?w=800&h=800&fit=crop",
                "description": "Elegant silver watch for formal occasions",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Wireless Earbuds Pro",
                "category": "gadgets",
                "price": 1499,
                "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800&h=800&fit=crop",
                "description": "Premium wireless earbuds with noise cancellation",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Smart Fitness Band",
                "category": "gadgets",
                "price": 899,
                "image": "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=800&h=800&fit=crop",
                "description": "Track your fitness goals with style",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Portable Speaker",
                "category": "gadgets",
                "price": 1299,
                "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800&h=800&fit=crop",
                "description": "Bluetooth speaker with premium sound quality",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Designer Denim Jacket",
                "category": "clothes",
                "price": 2499,
                "image": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=800&h=800&fit=crop",
                "description": "Trendy denim jacket for all seasons",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Premium Cotton T-Shirt",
                "category": "clothes",
                "price": 799,
                "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800&h=800&fit=crop",
                "description": "Comfortable cotton t-shirt in multiple colors",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Casual Hoodie",
                "category": "clothes",
                "price": 1499,
                "image": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=800&h=800&fit=crop",
                "description": "Warm and stylish hoodie for winter",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Running Sneakers",
                "category": "shoes",
                "price": 2199,
                "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&h=800&fit=crop",
                "description": "Comfortable running shoes with premium cushioning",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Casual Loafers",
                "category": "shoes",
                "price": 1799,
                "image": "https://images.unsplash.com/photo-1533867617858-e7b97e060509?w=800&h=800&fit=crop",
                "description": "Elegant loafers for casual and formal wear",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "High-Top Sneakers",
                "category": "shoes",
                "price": 2499,
                "image": "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=800&h=800&fit=crop",
                "description": "Stylish high-top sneakers for streetwear",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Leather Wallet",
                "category": "accessories",
                "price": 899,
                "image": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=800&h=800&fit=crop",
                "description": "Premium leather wallet with RFID protection",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Aviator Sunglasses",
                "category": "accessories",
                "price": 1299,
                "image": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=800&h=800&fit=crop",
                "description": "Classic aviator sunglasses with UV protection",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Designer Backpack",
                "category": "accessories",
                "price": 1999,
                "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800&h=800&fit=crop",
                "description": "Spacious backpack with laptop compartment",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Leather Belt",
                "category": "accessories",
                "price": 699,
                "image": "https://images.unsplash.com/photo-1624222247344-550fb60583bb?w=800&h=800&fit=crop",
                "description": "Classic leather belt for everyday wear",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            }
        ]
        
        await db.products.insert_many(products)
        
        # Seed Instagram Posts
        instagram_posts = [
            {
                "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&h=600&fit=crop",
                "likes": 234,
                "comments": 12,
                "createdAt": datetime.utcnow()
            },
            {
                "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&h=600&fit=crop",
                "likes": 456,
                "comments": 23,
                "createdAt": datetime.utcnow()
            },
            {
                "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=600&h=600&fit=crop",
                "likes": 189,
                "comments": 8,
                "createdAt": datetime.utcnow()
            },
            {
                "image": "https://images.unsplash.com/photo-1587836374852-dca8da20fd8d?w=600&h=600&fit=crop",
                "likes": 567,
                "comments": 34,
                "createdAt": datetime.utcnow()
            },
            {
                "image": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=600&h=600&fit=crop",
                "likes": 345,
                "comments": 19,
                "createdAt": datetime.utcnow()
            },
            {
                "image": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=600&h=600&fit=crop",
                "likes": 278,
                "comments": 15,
                "createdAt": datetime.utcnow()
            }
        ]
        
        await db.instagram_posts.insert_many(instagram_posts)
        
        return {
            "message": "Database seeded successfully",
            "productsCreated": len(products),
            "instagramPostsCreated": len(instagram_posts)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
