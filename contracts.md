# API Contracts & Backend Integration Plan

## Current Mock Data (to be replaced)
Location: `/app/frontend/src/mock.js`

### Products Data
- 16 products with categories: watches, gadgets, clothes, shoes, accessories
- Fields: id, name, category, price, image, description, inStock

### Instagram Posts Data
- 6 posts with likes and comments
- Fields: id, image, likes, comments

### Categories Data
- 6 categories including "all"
- Fields: id, name, icon

## Backend Implementation

### 1. MongoDB Models

#### Product Model
```python
{
    "_id": ObjectId,
    "name": str,
    "category": str,  # watches, gadgets, clothes, shoes, accessories
    "price": int,
    "image": str,  # URL
    "description": str,
    "inStock": bool,
    "createdAt": datetime,
    "updatedAt": datetime
}
```

#### Order Model
```python
{
    "_id": ObjectId,
    "items": [
        {
            "productId": ObjectId,
            "productName": str,
            "price": int,
            "quantity": int
        }
    ],
    "totalAmount": int,
    "customerPhone": str,  # WhatsApp number
    "status": str,  # pending, confirmed, completed, cancelled
    "orderDate": datetime
}
```

#### InstagramPost Model
```python
{
    "_id": ObjectId,
    "image": str,  # URL
    "likes": int,
    "comments": int,
    "postUrl": str,  # optional: link to actual Instagram post
    "createdAt": datetime
}
```

### 2. API Endpoints

#### Products
- `GET /api/products` - Get all products (with optional category filter)
  - Query params: `?category=watches`
  - Response: `{ "products": [...], "count": int }`

- `POST /api/products` - Create new product (admin)
  - Body: `{ name, category, price, image, description, inStock }`
  - Response: `{ "product": {...}, "message": "Product created" }`

- `PUT /api/products/{id}` - Update product (admin)
  - Body: `{ name?, category?, price?, image?, description?, inStock? }`
  - Response: `{ "product": {...}, "message": "Product updated" }`

- `DELETE /api/products/{id}` - Delete product (admin)
  - Response: `{ "message": "Product deleted" }`

#### Orders
- `POST /api/orders` - Create new order
  - Body: `{ items: [{productId, quantity}], customerPhone }`
  - Response: `{ "order": {...}, "message": "Order created" }`

- `GET /api/orders` - Get all orders (admin)
  - Response: `{ "orders": [...], "count": int }`

#### Instagram Posts
- `GET /api/instagram-posts` - Get all Instagram posts
  - Response: `{ "posts": [...] }`

- `POST /api/instagram-posts` - Create Instagram post (admin)
  - Body: `{ image, likes?, comments?, postUrl? }`
  - Response: `{ "post": {...}, "message": "Post created" }`

### 3. Seed Data
- Initialize database with the 16 products from mock.js
- Initialize with 6 Instagram posts from mock.js
- Create a seed script: `/api/seed` endpoint (one-time use)

## Frontend Integration Changes

### Files to Update

#### 1. `/app/frontend/src/pages/Home.jsx`
**Current:** Uses `products` and `instagramPosts` from `mock.js`

**Changes:**
- Import axios
- Fetch products on component mount: `GET /api/products?category={selectedCategory}`
- Fetch Instagram posts on component mount: `GET /api/instagram-posts`
- Add loading states
- Add error handling
- Remove mock imports

#### 2. `/app/frontend/src/components/Navbar.jsx`
**Current:** Uses `categories` from `mock.js`

**Changes:**
- Keep categories hardcoded (static data) OR
- Fetch from backend if dynamic categories needed

#### 3. Cart Functionality
**Current:** Cart managed in local state only

**Changes:**
- Keep cart in local state (good UX)
- On checkout (WhatsApp button click), POST order to backend
- Send order data: `POST /api/orders` with items and phone number
- Show success/error feedback

### Integration Steps

1. **Backend Setup**
   - Create models in `/app/backend/models/`
   - Create routes in `/app/backend/routes/`
   - Seed database with mock data
   - Test all endpoints

2. **Frontend Integration**
   - Update Home.jsx to fetch products and Instagram posts
   - Update cart checkout to POST orders
   - Add loading and error states
   - Remove mock.js imports
   - Test all flows

3. **Admin Features (Optional)**
   - Create admin endpoints for CRUD operations
   - Basic authentication for admin routes
   - Admin UI for managing products (future enhancement)

## Environment Variables

Backend (.env):
- `MONGO_URL` - Already configured
- `DB_NAME` - Already configured

Frontend (.env):
- `REACT_APP_BACKEND_URL` - Already configured

## Testing Checklist

### Backend
- [ ] Products API returns all products
- [ ] Products API filters by category
- [ ] Orders API creates new orders
- [ ] Instagram posts API returns posts
- [ ] Database seeding works correctly

### Frontend
- [ ] Products load from backend on page load
- [ ] Category filtering updates products from backend
- [ ] Cart checkout sends order to backend
- [ ] Instagram feed loads from backend
- [ ] Loading states display correctly
- [ ] Error handling works for failed API calls

## Notes
- All product data currently uses Unsplash images (external URLs) - no file upload needed
- WhatsApp integration remains frontend-only (opens WhatsApp with pre-filled message)
- Cart state remains in React (localStorage can be added for persistence)
- No authentication for now - can be added later if needed
