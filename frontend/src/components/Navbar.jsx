import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { ShoppingCart, Menu, X, Instagram } from 'lucide-react';
import { Button } from './ui/button';

const Navbar = ({ cartCount, categories }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const instagramUrl = process.env.REACT_APP_INSTAGRAM_URL || 'https://instagram.com';

  return (
    <nav className="bg-white shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
              C2B
            </div>
            <span className="text-sm text-gray-600 hidden sm:block">Click to Buy</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {categories.map(category => (
              <Link
                key={category.id}
                to={`/?category=${category.id}`}
                className="text-gray-700 hover:text-purple-600 font-medium transition-colors duration-200"
              >
                {category.name}
              </Link>
            ))}
          </div>

          {/* Right Side Actions */}
          <div className="flex items-center space-x-4">
            <a
              href={instagramUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-700 hover:text-pink-600 transition-colors duration-200"
            >
              <Instagram className="w-6 h-6" />
            </a>
            <Link to="/cart" className="relative">
              <Button variant="ghost" size="icon">
                <ShoppingCart className="w-6 h-6" />
                {cartCount > 0 && (
                  <span className="absolute -top-1 -right-1 bg-purple-600 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                    {cartCount}
                  </span>
                )}
              </Button>
            </Link>
            <button
              className="md:hidden"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-white border-t">
          <div className="px-4 py-4 space-y-3">
            {categories.map(category => (
              <Link
                key={category.id}
                to={`/?category=${category.id}`}
                className="block text-gray-700 hover:text-purple-600 font-medium py-2"
                onClick={() => setMobileMenuOpen(false)}
              >
                {category.name}
              </Link>
            ))}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
