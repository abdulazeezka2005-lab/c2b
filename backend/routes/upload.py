from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Optional
import os
import uuid
from pathlib import Path
import base64

router = APIRouter(prefix="/upload", tags=["upload"])

# Create uploads directory if it doesn't exist
UPLOADS_DIR = Path("/app/backend/uploads")
UPLOADS_DIR.mkdir(exist_ok=True)

@router.post("/image", response_model=dict)
async def upload_image(file: UploadFile = File(...)):
    """Upload product image"""
    try:
        # Validate file type
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Invalid file type. Only images allowed.")
        
        # Generate unique filename
        file_extension = file.filename.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = UPLOADS_DIR / unique_filename
        
        # Save file
        contents = await file.read()
        with open(file_path, 'wb') as f:
            f.write(contents)
        
        # Return relative URL with /api prefix for proper routing
        image_url = f"/api/uploads/{unique_filename}"
        
        return {
            "url": image_url,
            "filename": unique_filename,
            "message": "Image uploaded successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/image-base64", response_model=dict)
async def upload_image_base64(data: dict):
    """Upload image from base64 data"""


from fastapi.responses import FileResponse

@router.get("/image/{filename}")
async def get_image(filename: str):
    """Serve uploaded image"""
    file_path = UPLOADS_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path)
    try:
        base64_string = data.get('image')
        if not base64_string:
            raise HTTPException(status_code=400, detail="No image data provided")
        
        # Remove data URL prefix if present
        if 'base64,' in base64_string:
            base64_string = base64_string.split('base64,')[1]
        
        # Decode base64
        image_data = base64.b64decode(base64_string)
        
        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}.jpg"
        file_path = UPLOADS_DIR / unique_filename
        
        # Save file
        with open(file_path, 'wb') as f:
            f.write(image_data)
        
        # Return relative URL with /api prefix
        image_url = f"/api/uploads/{unique_filename}"
        
        return {
            "url": image_url,
            "filename": unique_filename,
            "message": "Image uploaded successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
