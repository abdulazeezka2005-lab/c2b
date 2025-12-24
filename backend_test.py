#!/usr/bin/env python3
"""
StyleHub Backend API Test Suite
Tests all backend API endpoints comprehensively
"""

import requests
import json
import os
from datetime import datetime

# Get backend URL from frontend .env file
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except Exception as e:
        print(f"Error reading frontend .env: {e}")
        return None

BASE_URL = get_backend_url()
if not BASE_URL:
    print("ERROR: Could not get REACT_APP_BACKEND_URL from frontend/.env")
    exit(1)

API_URL = f"{BASE_URL}/api"
print(f"Testing StyleHub API at: {API_URL}")

class StyleHubAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = {
            'passed': 0,
            'failed': 0,
            'errors': []
        }
        
    def log_result(self, test_name, success, message=""):
        if success:
            self.test_results['passed'] += 1
            print(f"✅ {test_name}")
        else:
            self.test_results['failed'] += 1
            self.test_results['errors'].append(f"{test_name}: {message}")
            print(f"❌ {test_name}: {message}")
    
    def test_health_check(self):
        """Test the health check endpoint"""
        try:
            response = self.session.get(f"{API_URL}/")
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'ok':
                    self.log_result("Health Check", True)
                    return True
                else:
                    self.log_result("Health Check", False, f"Status not ok: {data}")
                    return False
            else:
                self.log_result("Health Check", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Health Check", False, f"Exception: {str(e)}")
            return False
    
    def seed_database(self):
        """Seed the database with initial data"""
        try:
            response = self.session.post(f"{API_URL}/seed")
            if response.status_code == 200:
                data = response.json()
                self.log_result("Database Seeding", True, f"Message: {data.get('message', '')}")
                return True
            else:
                self.log_result("Database Seeding", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Database Seeding", False, f"Exception: {str(e)}")
            return False
    
    def test_get_all_products(self):
        """Test getting all products"""
        try:
            response = self.session.get(f"{API_URL}/products")
            if response.status_code == 200:
                data = response.json()
                products = data.get('products', [])
                count = data.get('count', 0)
                
                if len(products) == 16 and count == 16:
                    self.log_result("Get All Products", True, f"Found {count} products")
                    return products
                else:
                    self.log_result("Get All Products", False, f"Expected 16 products, got {count}")
                    return products
            else:
                self.log_result("Get All Products", False, f"Status code: {response.status_code}")
                return []
        except Exception as e:
            self.log_result("Get All Products", False, f"Exception: {str(e)}")
            return []
    
    def test_product_categories(self):
        """Test product filtering by categories"""
        categories = {
            'watches': 3,
            'gadgets': 3,
            'clothes': 3,
            'shoes': 3,
            'accessories': 4
        }
        
        for category, expected_count in categories.items():
            try:
                response = self.session.get(f"{API_URL}/products?category={category}")
                if response.status_code == 200:
                    data = response.json()
                    products = data.get('products', [])
                    count = data.get('count', 0)
                    
                    if count == expected_count:
                        self.log_result(f"Filter Products by {category}", True, f"Found {count} products")
                    else:
                        self.log_result(f"Filter Products by {category}", False, 
                                      f"Expected {expected_count}, got {count}")
                else:
                    self.log_result(f"Filter Products by {category}", False, 
                                  f"Status code: {response.status_code}")
            except Exception as e:
                self.log_result(f"Filter Products by {category}", False, f"Exception: {str(e)}")
    
    def test_create_product(self):
        """Test creating a new product"""
        test_product = {
            "name": "Test Smartwatch",
            "category": "watches",
            "price": 1999,
            "image": "https://example.com/test-watch.jpg",
            "description": "A test smartwatch for API testing",
            "inStock": True
        }
        
        try:
            response = self.session.post(f"{API_URL}/products", json=test_product)
            if response.status_code == 200:
                data = response.json()
                product = data.get('product', {})
                
                if product.get('name') == test_product['name'] and product.get('_id'):
                    self.log_result("Create Product", True, f"Created product with ID: {product['_id']}")
                    return product['_id']
                else:
                    self.log_result("Create Product", False, "Product data mismatch")
                    return None
            else:
                self.log_result("Create Product", False, f"Status code: {response.status_code}")
                return None
        except Exception as e:
            self.log_result("Create Product", False, f"Exception: {str(e)}")
            return None
    
    def test_update_product(self, product_id):
        """Test updating a product"""
        if not product_id:
            self.log_result("Update Product", False, "No product ID provided")
            return
        
        update_data = {
            "name": "Updated Test Smartwatch",
            "price": 2499
        }
        
        try:
            response = self.session.put(f"{API_URL}/products/{product_id}", json=update_data)
            if response.status_code == 200:
                data = response.json()
                product = data.get('product', {})
                
                if product.get('name') == update_data['name'] and product.get('price') == update_data['price']:
                    self.log_result("Update Product", True)
                else:
                    self.log_result("Update Product", False, "Update data mismatch")
            else:
                self.log_result("Update Product", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_result("Update Product", False, f"Exception: {str(e)}")
    
    def test_delete_product(self, product_id):
        """Test deleting a product"""
        if not product_id:
            self.log_result("Delete Product", False, "No product ID provided")
            return
        
        try:
            response = self.session.delete(f"{API_URL}/products/{product_id}")
            if response.status_code == 200:
                data = response.json()
                if "deleted successfully" in data.get('message', ''):
                    self.log_result("Delete Product", True)
                else:
                    self.log_result("Delete Product", False, f"Unexpected message: {data.get('message')}")
            else:
                self.log_result("Delete Product", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_result("Delete Product", False, f"Exception: {str(e)}")
    
    def test_invalid_product_operations(self):
        """Test error handling for invalid product operations"""
        invalid_id = "invalid_id_123"
        
        # Test update with invalid ID
        try:
            response = self.session.put(f"{API_URL}/products/{invalid_id}", json={"name": "Test"})
            if response.status_code == 400:
                self.log_result("Invalid Product ID - Update", True)
            else:
                self.log_result("Invalid Product ID - Update", False, f"Expected 400, got {response.status_code}")
        except Exception as e:
            self.log_result("Invalid Product ID - Update", False, f"Exception: {str(e)}")
        
        # Test delete with invalid ID
        try:
            response = self.session.delete(f"{API_URL}/products/{invalid_id}")
            if response.status_code == 400:
                self.log_result("Invalid Product ID - Delete", True)
            else:
                self.log_result("Invalid Product ID - Delete", False, f"Expected 400, got {response.status_code}")
        except Exception as e:
            self.log_result("Invalid Product ID - Delete", False, f"Exception: {str(e)}")
    
    def test_create_order(self):
        """Test creating an order"""
        test_order = {
            "items": [
                {
                    "productId": "test_product_1",
                    "productName": "Test Product 1",
                    "price": 1999,
                    "quantity": 2
                },
                {
                    "productId": "test_product_2", 
                    "productName": "Test Product 2",
                    "price": 2999,
                    "quantity": 1
                }
            ],
            "customerPhone": "+1234567890"
        }
        
        expected_total = (1999 * 2) + (2999 * 1)  # 6997
        
        try:
            response = self.session.post(f"{API_URL}/orders", json=test_order)
            if response.status_code == 200:
                data = response.json()
                order = data.get('order', {})
                
                if (order.get('totalAmount') == expected_total and 
                    order.get('status') == 'pending' and
                    order.get('_id')):
                    self.log_result("Create Order", True, f"Order total: {order['totalAmount']}")
                    return order['_id']
                else:
                    self.log_result("Create Order", False, f"Order data mismatch. Total: {order.get('totalAmount')}, Expected: {expected_total}")
                    return None
            else:
                self.log_result("Create Order", False, f"Status code: {response.status_code}")
                return None
        except Exception as e:
            self.log_result("Create Order", False, f"Exception: {str(e)}")
            return None
    
    def test_get_orders(self):
        """Test getting all orders"""
        try:
            response = self.session.get(f"{API_URL}/orders")
            if response.status_code == 200:
                data = response.json()
                orders = data.get('orders', [])
                count = data.get('count', 0)
                
                if len(orders) >= 1:  # At least the test order we created
                    self.log_result("Get All Orders", True, f"Found {count} orders")
                else:
                    self.log_result("Get All Orders", False, f"Expected at least 1 order, got {count}")
            else:
                self.log_result("Get All Orders", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_result("Get All Orders", False, f"Exception: {str(e)}")
    
    def test_get_instagram_posts(self):
        """Test getting Instagram posts"""
        try:
            response = self.session.get(f"{API_URL}/instagram-posts")
            if response.status_code == 200:
                data = response.json()
                posts = data.get('posts', [])
                
                if len(posts) == 6:
                    self.log_result("Get Instagram Posts", True, f"Found {len(posts)} posts")
                else:
                    self.log_result("Get Instagram Posts", False, f"Expected 6 posts, got {len(posts)}")
            else:
                self.log_result("Get Instagram Posts", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_result("Get Instagram Posts", False, f"Exception: {str(e)}")
    
    def test_create_instagram_post(self):
        """Test creating an Instagram post"""
        test_post = {
            "image": "https://example.com/test-post.jpg",
            "likes": 100,
            "comments": 5,
            "postUrl": "https://instagram.com/p/test123"
        }
        
        try:
            response = self.session.post(f"{API_URL}/instagram-posts", json=test_post)
            if response.status_code == 200:
                data = response.json()
                post = data.get('post', {})
                
                if (post.get('image') == test_post['image'] and 
                    post.get('likes') == test_post['likes'] and
                    post.get('_id')):
                    self.log_result("Create Instagram Post", True, f"Created post with ID: {post['_id']}")
                else:
                    self.log_result("Create Instagram Post", False, "Post data mismatch")
            else:
                self.log_result("Create Instagram Post", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_result("Create Instagram Post", False, f"Exception: {str(e)}")
    
    def run_all_tests(self):
        """Run all API tests"""
        print("=" * 60)
        print("StyleHub Backend API Test Suite")
        print("=" * 60)
        
        # 1. Health check
        if not self.test_health_check():
            print("❌ Health check failed. Stopping tests.")
            return self.test_results
        
        # 2. Seed database
        self.seed_database()
        
        # 3. Product tests
        print("\n--- Product API Tests ---")
        products = self.test_get_all_products()
        self.test_product_categories()
        
        # CRUD operations
        product_id = self.test_create_product()
        self.test_update_product(product_id)
        self.test_delete_product(product_id)
        
        # Error handling
        self.test_invalid_product_operations()
        
        # 4. Order tests
        print("\n--- Order API Tests ---")
        order_id = self.test_create_order()
        self.test_get_orders()
        
        # 5. Instagram posts tests
        print("\n--- Instagram Posts API Tests ---")
        self.test_get_instagram_posts()
        self.test_create_instagram_post()
        
        return self.test_results
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {self.test_results['passed']}")
        print(f"❌ Failed: {self.test_results['failed']}")
        
        if self.test_results['errors']:
            print("\nFAILED TESTS:")
            for error in self.test_results['errors']:
                print(f"  • {error}")
        
        success_rate = (self.test_results['passed'] / 
                       (self.test_results['passed'] + self.test_results['failed'])) * 100
        print(f"\nSuccess Rate: {success_rate:.1f}%")
        
        if self.test_results['failed'] == 0:
            print("\n🎉 All tests passed! StyleHub API is working correctly.")
        else:
            print(f"\n⚠️  {self.test_results['failed']} test(s) failed. Please check the issues above.")

if __name__ == "__main__":
    tester = StyleHubAPITester()
    results = tester.run_all_tests()
    tester.print_summary()