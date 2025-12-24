from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional, List
from models.product import Product, ProductCreate, ProductUpdate
from bson import ObjectId
from datetime import datetime
import os
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter(prefix="/products", tags=["products"])

def get_database():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    return client[os.environ['DB_NAME']]

@router.get("", response_model=dict)
async def get_products(category: Optional[str] = Query(None)):
    try:
        query = {}
        if category and category != "all":
            query["category"] = category
        
        products = await db.products.find(query).to_list(1000)
        
        # Convert ObjectId to string
        for product in products:
            product["_id"] = str(product["_id"])
        
        return {"products": products, "count": len(products)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("", response_model=dict)
async def create_product(product: ProductCreate):
    try:
        product_dict = product.dict()
        product_dict["createdAt"] = datetime.utcnow()
        product_dict["updatedAt"] = datetime.utcnow()
        
        result = await db.products.insert_one(product_dict)
        product_dict["_id"] = str(result.inserted_id)
        
        return {"product": product_dict, "message": "Product created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{product_id}", response_model=dict)
async def update_product(product_id: str, product: ProductUpdate):
    try:
        if not ObjectId.is_valid(product_id):
            raise HTTPException(status_code=400, detail="Invalid product ID")
        
        update_data = {k: v for k, v in product.dict().items() if v is not None}
        update_data["updatedAt"] = datetime.utcnow()
        
        result = await db.products.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        
        updated_product = await db.products.find_one({"_id": ObjectId(product_id)})
        updated_product["_id"] = str(updated_product["_id"])
        
        return {"product": updated_product, "message": "Product updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{product_id}", response_model=dict)
async def delete_product(product_id: str):
    try:
        if not ObjectId.is_valid(product_id):
            raise HTTPException(status_code=400, detail="Invalid product ID")
        
        result = await db.products.delete_one({"_id": ObjectId(product_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return {"message": "Product deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
