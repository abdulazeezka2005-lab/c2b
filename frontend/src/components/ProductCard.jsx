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
    <Card className="overflow-hidden hover:shadow-lg transition-shadow duration-200 bg-white border-2 border-gray-100">
      <div className="relative overflow-hidden aspect-square bg-gray-100">
        <img
          src={getImageUrl(product.image)}
          alt={product.name}
          className="w-full h-full object-cover"
          onError={(e) => {
            console.error('Image load error for:', product.name, product.image);
            e.target.src = 'https://via.placeholder.com/400?text=Product+Image';
          }}
        />
        {product.inStock ? (
          <span className="absolute top-3 right-3 bg-green-600 text-white text-xs font-bold px-3 py-1.5 rounded">
            IN STOCK
          </span>
        ) : (
          <span className="absolute top-3 right-3 bg-red-600 text-white text-xs font-bold px-3 py-1.5 rounded">
            OUT OF STOCK
          </span>
        )}
      </div>
      <CardContent className="p-4">
        <h3 className="font-bold text-lg text-gray-900 mb-2 line-clamp-2 min-h-[3.5rem]">{product.name}</h3>
        <p className="text-sm text-gray-600 mb-3 line-clamp-2 min-h-[2.5rem]">{product.description}</p>
        <div className="mb-4">
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-bold text-purple-600">₹{product.price}</span>
            <span className="text-sm text-gray-500 line-through">₹{Math.round(product.price * 1.3)}</span>
          </div>
          <span className="text-xs text-green-600 font-semibold">Save {Math.round(((product.price * 1.3 - product.price) / (product.price * 1.3)) * 100)}%</span>
        </div>
        <div className="space-y-2">
          <Button
            onClick={() => onAddToCart(product)}
            className="w-full bg-purple-600 hover:bg-purple-700 text-white font-semibold py-5"
            disabled={!product.inStock}
          >
            <ShoppingCart className="w-4 h-4 mr-2" />
            Add to Cart
          </Button>
          <Button
            onClick={() => onWhatsAppOrder(product)}
            className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-5"
            disabled={!product.inStock}
          >
            <MessageCircle className="w-4 h-4 mr-2" />
            Buy on WhatsApp
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default ProductCard;
