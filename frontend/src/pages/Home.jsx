import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import axios from 'axios';
import Hero from '../components/Hero';
import ProductCard from '../components/ProductCard';
import ProductDetailModal from '../components/ProductDetailModal';
import InstagramFeed from '../components/InstagramFeed';
import { categories } from '../mock';
import { Button } from '../components/ui/button';
import { useToast } from '../hooks/use-toast';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Home = ({ cart, setCart }) => {
  const [searchParams] = useSearchParams();
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [products, setProducts] = useState([]);
  const [instagramPosts, setInstagramPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [showProductModal, setShowProductModal] = useState(false);
  const { toast } = useToast();

  // Fetch products when category changes
  useEffect(() => {
    const category = searchParams.get('category');
    if (category) {
      setSelectedCategory(category);
    }
  }, [searchParams]);

  useEffect(() => {
    fetchProducts();
    fetchInstagramPosts();
  }, [selectedCategory]);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const url = selectedCategory === 'all' 
        ? `${API}/products` 
        : `${API}/products?category=${selectedCategory}`;
      const response = await axios.get(url);
      setProducts(response.data.products);
      setError(null);
    } catch (err) {
      console.error('Error fetching products:', err);
      setError('Failed to load products');
    } finally {
      setLoading(false);
    }
  };

  const fetchInstagramPosts = async () => {
    try {
      const response = await axios.get(`${API}/instagram-posts`);
      setInstagramPosts(response.data.posts);
    } catch (err) {
      console.error('Error fetching Instagram posts:', err);
    }
  };

  const handleAddToCart = (product, quantity = 1) => {
    const existingItem = cart.find(item => item._id === product._id);
    if (existingItem) {
      setCart(cart.map(item =>
        item._id === product._id
          ? { ...item, quantity: item.quantity + quantity }
          : item
      ));
    } else {
      setCart([...cart, { ...product, quantity }]);
    }
  };

  const handleWhatsAppOrder = (product) => {
    const whatsappPhone = process.env.REACT_APP_WHATSAPP_PHONE || '1234567890';
    const message = `Hi! I'm interested in:

*${product.name}*
Price: ₹${product.price}

Please share more details.`;
    const whatsappUrl = `https://wa.me/${whatsappPhone}?text=${encodeURIComponent(message)}`;
    window.open(whatsappUrl, '_blank');
  };

  const handleProductClick = (product) => {
    setSelectedProduct(product);
    setShowProductModal(true);
  };

  return (
    <div>
      <Hero />

      {/* Category Filter */}
      <div id="products" className="bg-gray-50 py-6 border-y-2 border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4 text-center">Shop by Category</h2>
          <div className="flex overflow-x-auto gap-3 pb-2 scrollbar-hide justify-center">
            {categories.map(category => (
              <Button
                key={category.id}
                onClick={() => setSelectedCategory(category.id)}
                variant={selectedCategory === category.id ? 'default' : 'outline'}
                className={`whitespace-nowrap transition-all duration-200 font-semibold ${
                  selectedCategory === category.id
                    ? 'bg-purple-600 text-white hover:bg-purple-700 shadow-md'
                    : 'bg-white hover:bg-purple-50 hover:border-purple-600 hover:text-purple-600 border-2'
                }`}
              >
                {category.name}
              </Button>
            ))}
          </div>
        </div>
      </div>

      {/* Products Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 bg-white">
        <div className="mb-8 text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            {categories.find(c => c.id === selectedCategory)?.name || 'All Products'}
          </h2>
          {loading ? (
            <p className="text-gray-600">Loading products...</p>
          ) : error ? (
            <p className="text-red-600">{error}</p>
          ) : (
            <p className="text-gray-600 text-lg">{products.length} products available</p>
          )}
        </div>
        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {[1, 2, 3, 4].map(i => (
              <div key={i} className="bg-gray-200 animate-pulse h-96 rounded-lg"></div>
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {products.map(product => (
              <ProductCard
                key={product._id}
                product={product}
                onAddToCart={handleAddToCart}
                onWhatsAppOrder={handleWhatsAppOrder}
              />
            ))}
          </div>
        )}
      </div>

      {/* Instagram Feed */}
      <InstagramFeed posts={instagramPosts} />

      {/* Product Detail Modal */}
      {showProductModal && selectedProduct && (
        <ProductDetailModal
          product={selectedProduct}
          onClose={() => setShowProductModal(false)}
          onAddToCart={handleAddToCart}
          onWhatsAppOrder={handleWhatsAppOrder}
        />
      )}
    </div>
  );
};

export default Home;
