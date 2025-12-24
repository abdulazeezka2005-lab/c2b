import React from 'react';
import { ShoppingCart, MessageCircle } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent } from './ui/card';

const ProductCard = ({ product, onAddToCart, onWhatsAppOrder }) => {
  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
  
  // Handle image URL - add backend URL if it's a relative path
  const getImageUrl = (imageUrl) => {
    if (!imageUrl) return 'https://via.placeholder.com/400';
    if (imageUrl.startsWith('http')) return imageUrl;
    // Handle API upload paths
    if (imageUrl.startsWith('/api/')) {
      return `${BACKEND_URL}${imageUrl}`;
    }
    return imageUrl;
  };

  return (
    <Card className="group overflow-hidden hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
      <div className="relative overflow-hidden aspect-square">
        <img
          src={getImageUrl(product.image)}
          alt={product.name}
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
          onError={(e) => {
            console.error('Image load error for:', product.name, product.image);
            e.target.src = 'https://via.placeholder.com/400?text=Product+Image';
          }}
        />
        {product.inStock ? (
          <span className="absolute top-3 right-3 bg-green-500 text-white text-xs px-3 py-1 rounded-full">
            In Stock
          </span>
        ) : (
          <span className="absolute top-3 right-3 bg-red-500 text-white text-xs px-3 py-1 rounded-full">
            Out of Stock
          </span>
        )}
      </div>
      <CardContent className="p-4">
        <h3 className="font-semibold text-lg text-gray-900 mb-1">{product.name}</h3>
        <p className="text-sm text-gray-600 mb-3 line-clamp-2">{product.description}</p>
        <div className="flex items-center justify-between mb-4">
          <span className="text-2xl font-bold text-purple-600">₹{product.price}</span>
        </div>
        <div className="flex gap-2">
          <Button
            onClick={() => onAddToCart(product)}
            className="flex-1 bg-purple-600 hover:bg-purple-700 text-white"
            disabled={!product.inStock}
          >
            <ShoppingCart className="w-4 h-4 mr-2" />
            Add to Cart
          </Button>
          <Button
            onClick={() => onWhatsAppOrder(product)}
            variant="outline"
            className="border-green-500 text-green-600 hover:bg-green-50"
            disabled={!product.inStock}
          >
            <MessageCircle className="w-4 h-4" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default ProductCard;
