import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import Hero from '../components/Hero';
import ProductCard from '../components/ProductCard';
import InstagramFeed from '../components/InstagramFeed';
import { products, instagramPosts, categories } from '../mock';
import { Button } from '../components/ui/button';
import { useToast } from '../hooks/use-toast';

const Home = ({ cart, setCart }) => {
  const [searchParams] = useSearchParams();
  const [selectedCategory, setSelectedCategory] = useState('all');
  const { toast } = useToast();

  useEffect(() => {
    const category = searchParams.get('category');
    if (category) {
      setSelectedCategory(category);
    }
  }, [searchParams]);

  const filteredProducts = selectedCategory === 'all'
    ? products
    : products.filter(p => p.category === selectedCategory);

  const handleAddToCart = (product) => {
    const existingItem = cart.find(item => item.id === product.id);
    if (existingItem) {
      setCart(cart.map(item =>
        item.id === product.id
          ? { ...item, quantity: item.quantity + 1 }
          : item
      ));
    } else {
      setCart([...cart, { ...product, quantity: 1 }]);
    }
    toast({
      title: "Added to cart!",
      description: `${product.name} has been added to your cart.`,
    });
  };

  const handleWhatsAppOrder = (product) => {
    const message = `Hi! I'm interested in:

*${product.name}*
Price: ₹${product.price}

Please share more details.`;
    const whatsappUrl = `https://wa.me/1234567890?text=${encodeURIComponent(message)}`;
    window.open(whatsappUrl, '_blank');
  };

  return (
    <div>
      <Hero />

      {/* Category Filter */}
      <div id="products" className="bg-white py-8 sticky top-16 z-40 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex overflow-x-auto gap-3 pb-2 scrollbar-hide">
            {categories.map(category => (
              <Button
                key={category.id}
                onClick={() => setSelectedCategory(category.id)}
                variant={selectedCategory === category.id ? 'default' : 'outline'}
                className={`whitespace-nowrap transition-all duration-200 ${
                  selectedCategory === category.id
                    ? 'bg-purple-600 text-white hover:bg-purple-700'
                    : 'hover:border-purple-600 hover:text-purple-600'
                }`}
              >
                {category.name}
              </Button>
            ))}
          </div>
        </div>
      </div>

      {/* Products Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900">
            {categories.find(c => c.id === selectedCategory)?.name || 'All Products'}
          </h2>
          <p className="text-gray-600">{filteredProducts.length} products available</p>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {filteredProducts.map(product => (
            <ProductCard
              key={product.id}
              product={product}
              onAddToCart={handleAddToCart}
              onWhatsAppOrder={handleWhatsAppOrder}
            />
          ))}
        </div>
      </div>

      {/* Instagram Feed */}
      <InstagramFeed posts={instagramPosts} />
    </div>
  );
};

export default Home;
