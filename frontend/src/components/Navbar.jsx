import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { ShoppingCart, Menu, X, Instagram, Phone } from 'lucide-react';
import { Button } from './ui/button';

const Navbar = ({ cartCount, categories }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const instagramUrl = process.env.REACT_APP_INSTAGRAM_URL || 'https://instagram.com';
  const contactPhone = process.env.REACT_APP_CONTACT_PHONE || '+91 6380832058';

  return (
    <nav className="bg-white shadow-md sticky top-0 z-50 border-b-2 border-gray-200">
      {/* Top Bar */}
      <div className="bg-purple-600 text-white py-2">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center text-sm">
            <div className="flex items-center gap-4">
              <span className="hidden sm:inline">✓ 100% Genuine Products</span>
              <span className="hidden md:inline">✓ Fast Delivery</span>
            </div>
            <div className="flex items-center gap-4">
              <a href={`tel:${contactPhone}`} className="flex items-center hover:underline">
                <Phone className="w-3 h-3 mr-1" />
                {contactPhone}
              </a>
              <a href={instagramUrl} target="_blank" rel="noopener noreferrer" className="hover:underline">
                <Instagram className="w-4 h-4" />
              </a>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="text-2xl font-bold text-purple-600">
              C2B
            </div>
            <span className="text-sm text-gray-600 hidden sm:block font-semibold">Click to Buy</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-6">
            {categories.slice(0, 6).map(category => (
              <Link
                key={category.id}
                to={`/?category=${category.id}`}
                className="text-gray-700 hover:text-purple-600 font-medium transition-colors duration-200 hover:underline"
              >
                {category.name}
              </Link>
            ))}
          </div>

          {/* Right Side Actions */}
          <div className="flex items-center space-x-4">
            <Link to="/cart" className="relative">
              <Button variant="ghost" size="icon" className="hover:bg-purple-50">
                <ShoppingCart className="w-6 h-6 text-gray-700" />
                {cartCount > 0 && (
                  <span className="absolute -top-1 -right-1 bg-red-600 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center font-bold">
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
        <div className="md:hidden bg-white border-t-2 border-gray-200">
          <div className="px-4 py-4 space-y-3">
            {categories.map(category => (
              <Link
                key={category.id}
                to={`/?category=${category.id}`}
                className="block text-gray-700 hover:text-purple-600 font-medium py-2 hover:bg-purple-50 px-3 rounded"
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
