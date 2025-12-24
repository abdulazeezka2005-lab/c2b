from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path

# Import routes
from routes.products import router as products_router
from routes.orders import router as orders_router
from routes.instagram_posts import router as instagram_router
from routes.seed import router as seed_router
from routes.admin import router as admin_router
from routes.reviews import router as reviews_router
from routes.payments import router as payments_router
from routes.upload import router as upload_router


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Health check route
@api_router.get("/")
async def root():
    return {"message": "StyleHub API is running", "status": "ok"}

# Include all routers
api_router.include_router(products_router)
api_router.include_router(orders_router)
api_router.include_router(instagram_router)
api_router.include_router(seed_router)
api_router.include_router(admin_router)
api_router.include_router(reviews_router)
api_router.include_router(payments_router)
api_router.include_router(upload_router)

# Include the router in the main app
app.include_router(api_router)

# Serve uploaded files
uploads_dir = Path("/app/backend/uploads")
uploads_dir.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(uploads_dir)), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()