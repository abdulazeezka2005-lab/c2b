from fastapi import APIRouter, HTTPException
from datetime import datetime
import os
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter(prefix="/seed", tags=["seed"])

def get_database():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    return client[os.environ['DB_NAME']]

@router.post("", response_model=dict)
async def seed_database():
    try:
        db = get_database()
        # Check if already seeded
        existing_products = await db.products.count_documents({})
        
        # Always allow re-seeding to add new categories
        
        # Seed Products with NEW categories
        new_products = [
            # Electronics
            {
                "name": "Wireless Keyboard",
                "category": "electronics",
                "price": 1599,
                "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&h=800&fit=crop",
                "description": "Mechanical wireless keyboard with RGB lighting",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Gaming Mouse",
                "category": "electronics",
                "price": 999,
                "image": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800&h=800&fit=crop",
                "description": "High precision gaming mouse with customizable buttons",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "USB-C Hub",
                "category": "electronics",
                "price": 1299,
                "image": "https://images.unsplash.com/photo-1625948515291-69613efd103f?w=800&h=800&fit=crop",
                "description": "7-in-1 USB-C hub with HDMI and card reader",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            # Home Decor
            {
                "name": "Modern Table Lamp",
                "category": "homedecor",
                "price": 2499,
                "image": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800&h=800&fit=crop",
                "description": "Minimalist LED table lamp with touch control",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Wall Art Canvas",
                "category": "homedecor",
                "price": 1999,
                "image": "https://images.unsplash.com/photo-1513519245088-0e12902e35ca?w=800&h=800&fit=crop",
                "description": "Abstract wall art canvas print",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Decorative Cushions",
                "category": "homedecor",
                "price": 799,
                "image": "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=800&h=800&fit=crop",
                "description": "Set of 2 premium decorative cushions",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            # Beauty Products
            {
                "name": "Skincare Set",
                "category": "beauty",
                "price": 2999,
                "image": "https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=800&h=800&fit=crop",
                "description": "Complete skincare routine set",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Hair Dryer Pro",
                "category": "beauty",
                "price": 3499,
                "image": "https://images.unsplash.com/photo-1522338140262-f46f5913618a?w=800&h=800&fit=crop",
                "description": "Professional ionic hair dryer",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Makeup Brush Set",
                "category": "beauty",
                "price": 1499,
                "image": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=800&h=800&fit=crop",
                "description": "Professional 12-piece makeup brush set",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            # Jewelry
            {
                "name": "Silver Bracelet",
                "category": "jewelry",
                "price": 1999,
                "image": "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=800&h=800&fit=crop",
                "description": "Sterling silver chain bracelet",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Pearl Necklace",
                "category": "jewelry",
                "price": 3499,
                "image": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=800&h=800&fit=crop",
                "description": "Classic pearl necklace",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Gold Earrings",
                "category": "jewelry",
                "price": 2499,
                "image": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=800&h=800&fit=crop",
                "description": "18k gold plated drop earrings",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            # Sports Equipment
            {
                "name": "Yoga Mat Premium",
                "category": "sports",
                "price": 1299,
                "image": "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=800&h=800&fit=crop",
                "description": "Non-slip premium yoga mat",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Resistance Bands",
                "category": "sports",
                "price": 699,
                "image": "https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=800&h=800&fit=crop",
                "description": "Set of 5 resistance bands for workout",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Dumbbell Set",
                "category": "sports",
                "price": 2999,
                "image": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800&h=800&fit=crop",
                "description": "Adjustable dumbbell set 5-25kg",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            }
        ]
        
        if existing_products == 0:
            # First time seeding - add original products
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

@router.post("/add-new-categories", response_model=dict)
async def add_new_categories():
    """Add products from new categories"""
    try:
        db = get_database()
        
        # Check if new category products already exist
        electronics_count = await db.products.count_documents({"category": "electronics"})
        if electronics_count > 0:
            return {"message": "New categories already added", "skipped": True}
        
        new_products = [
            # Electronics
            {
                "name": "Wireless Keyboard",
                "category": "electronics",
                "price": 1599,
                "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&h=800&fit=crop",
                "description": "Mechanical wireless keyboard with RGB lighting",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Gaming Mouse",
                "category": "electronics",
                "price": 999,
                "image": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=800&h=800&fit=crop",
                "description": "High precision gaming mouse with customizable buttons",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "USB-C Hub",
                "category": "electronics",
                "price": 1299,
                "image": "https://images.unsplash.com/photo-1625948515291-69613efd103f?w=800&h=800&fit=crop",
                "description": "7-in-1 USB-C hub with HDMI and card reader",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            # Home Decor
            {
                "name": "Modern Table Lamp",
                "category": "homedecor",
                "price": 2499,
                "image": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800&h=800&fit=crop",
                "description": "Minimalist LED table lamp with touch control",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Wall Art Canvas",
                "category": "homedecor",
                "price": 1999,
                "image": "https://images.unsplash.com/photo-1513519245088-0e12902e35ca?w=800&h=800&fit=crop",
                "description": "Abstract wall art canvas print",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Decorative Cushions",
                "category": "homedecor",
                "price": 799,
                "image": "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=800&h=800&fit=crop",
                "description": "Set of 2 premium decorative cushions",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            # Beauty Products
            {
                "name": "Skincare Set",
                "category": "beauty",
                "price": 2999,
                "image": "https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=800&h=800&fit=crop",
                "description": "Complete skincare routine set",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Hair Dryer Pro",
                "category": "beauty",
                "price": 3499,
                "image": "https://images.unsplash.com/photo-1522338140262-f46f5913618a?w=800&h=800&fit=crop",
                "description": "Professional ionic hair dryer",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Makeup Brush Set",
                "category": "beauty",
                "price": 1499,
                "image": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=800&h=800&fit=crop",
                "description": "Professional 12-piece makeup brush set",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            # Jewelry
            {
                "name": "Silver Bracelet",
                "category": "jewelry",
                "price": 1999,
                "image": "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=800&h=800&fit=crop",
                "description": "Sterling silver chain bracelet",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Pearl Necklace",
                "category": "jewelry",
                "price": 3499,
                "image": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=800&h=800&fit=crop",
                "description": "Classic pearl necklace",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Gold Earrings",
                "category": "jewelry",
                "price": 2499,
                "image": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=800&h=800&fit=crop",
                "description": "18k gold plated drop earrings",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            # Sports Equipment
            {
                "name": "Yoga Mat Premium",
                "category": "sports",
                "price": 1299,
                "image": "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=800&h=800&fit=crop",
                "description": "Non-slip premium yoga mat",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Resistance Bands",
                "category": "sports",
                "price": 699,
                "image": "https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=800&h=800&fit=crop",
                "description": "Set of 5 resistance bands for workout",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            },
            {
                "name": "Dumbbell Set",
                "category": "sports",
                "price": 2999,
                "image": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800&h=800&fit=crop",
                "description": "Adjustable dumbbell set 5-25kg",
                "inStock": True,
                "createdAt": datetime.utcnow(),
                "updatedAt": datetime.utcnow()
            }
        ]
        
        await db.products.insert_many(new_products)
        
        return {
            "message": "New categories added successfully",
            "productsCreated": len(new_products),
            "categories": ["electronics", "homedecor", "beauty", "jewelry", "sports"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

