import React from 'react';
import { ShoppingCart, MessageCircle, Eye } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent } from './ui/card';

const ProductCard = ({ product, onAddToCart, onWhatsAppOrder, onProductClick }) => {
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
    <Card className="overflow-hidden hover:shadow-lg transition-shadow duration-200 bg-white border-2 border-gray-100 cursor-pointer">
      <div 
        className="relative overflow-hidden aspect-square bg-gray-100"
        onClick={() => onProductClick(product)}
      >
        <img
          src={getImageUrl(product.image)}
          alt={product.name}
          className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
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
        <div className=\"absolute inset-0 bg-black bg-opacity-0 hover:bg-opacity-10 transition-all duration-200 flex items-center justify-center\">\n          <div className=\"opacity-0 hover:opacity-100 transition-opacity duration-200\">\n            <Eye className=\"w-12 h-12 text-white drop-shadow-lg\" />\n          </div>\n        </div>
      </div>
      <CardContent className=\"p-4\">
        <h3 className=\"font-bold text-lg text-gray-900 mb-2 line-clamp-2 min-h-[3.5rem] cursor-pointer hover:text-purple-600\" onClick={() => onProductClick(product)}>{product.name}</h3>
        <p className=\"text-sm text-gray-600 mb-3 line-clamp-2 min-h-[2.5rem]\">{product.description}</p>
        <div className=\"mb-4\">
          <div className=\"flex items-baseline gap-2\">
            <span className=\"text-2xl font-bold text-purple-600\">\u20b9{product.price}</span>
            <span className=\"text-sm text-gray-500 line-through\">\u20b9{Math.round(product.price * 1.3)}</span>
          </div>
          <span className=\"text-xs text-green-600 font-semibold\">Save {Math.round(((product.price * 1.3 - product.price) / (product.price * 1.3)) * 100)}%</span>
        </div>
        <Button
          onClick={() => onProductClick(product)}
          className=\"w-full bg-purple-600 hover:bg-purple-700 text-white font-semibold py-5 text-base\"
          disabled={!product.inStock}
        >
          <Eye className=\"w-4 h-4 mr-2\" />
          View & Buy Now
        </Button>
      </CardContent>
    </Card>
  );
};

export default ProductCard;
