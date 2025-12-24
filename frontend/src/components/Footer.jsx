import React from 'react';
import { Instagram, MessageCircle, Mail, Phone } from 'lucide-react';
import { Link } from 'react-router-dom';

const Footer = () => {
  const instagramUrl = process.env.REACT_APP_INSTAGRAM_URL || 'https://instagram.com';
  const whatsappPhone = process.env.REACT_APP_WHATSAPP_PHONE || '1234567890';
  const contactPhone = process.env.REACT_APP_CONTACT_PHONE || '+91 1234567890';
  const contactEmail = process.env.REACT_APP_CONTACT_EMAIL || 'info@stylehub.com';
  
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div>
            <h3 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent mb-4">
              C2B
            </h3>
            <p className="text-gray-400 text-sm">
              Click to Buy - Your one-stop shop for premium watches, gadgets, fashion, and accessories.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li><Link to="/?category=all" className="hover:text-white transition-colors">All Products</Link></li>
              <li><Link to="/?category=watches" className="hover:text-white transition-colors">Watches</Link></li>
              <li><Link to="/?category=gadgets" className="hover:text-white transition-colors">Gadgets</Link></li>
              <li><Link to="/?category=clothes" className="hover:text-white transition-colors">Clothes</Link></li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="font-semibold mb-4">Contact Us</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li className="flex items-center">
                <Phone className="w-4 h-4 mr-2" />
                <span>{contactPhone}</span>
              </li>
              <li className="flex items-center">
                <Mail className="w-4 h-4 mr-2" />
                <span>{contactEmail}</span>
              </li>
            </ul>
          </div>

          {/* Social Media */}
          <div>
            <h4 className="font-semibold mb-4">Follow Us</h4>
            <div className="flex space-x-4">
              <a
                href={instagramUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="bg-gradient-to-r from-purple-500 to-pink-500 p-3 rounded-full hover:from-purple-600 hover:to-pink-600 transition-all duration-200"
              >
                <Instagram className="w-5 h-5" />
              </a>
              <a
                href={`https://wa.me/${whatsappPhone}`}
                target="_blank"
                rel="noopener noreferrer"
                className="bg-green-500 p-3 rounded-full hover:bg-green-600 transition-all duration-200"
              >
                <MessageCircle className="w-5 h-5" />
              </a>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-sm text-gray-400">
          <p>&copy; {new Date().getFullYear()} C2B - Click to Buy. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
