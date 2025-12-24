import React from 'react';
import { Button } from './ui/button';
import { ArrowRight, MessageCircle, ShoppingBag } from 'lucide-react';

const Hero = () => {
  const whatsappPhone = process.env.REACT_APP_WHATSAPP_PHONE || '916380832058';
  
  const scrollToProducts = () => {
    document.getElementById('products')?.scrollIntoView({ behavior: 'smooth' });
  };

  const openWhatsApp = () => {
    const message = "Hi! I'm interested in your products. Can you help me?";
    const whatsappUrl = `https://wa.me/${whatsappPhone}?text=${encodeURIComponent(message)}`;
    window.open(whatsappUrl, '_blank');
  };

  return (
    <div className="relative bg-white border-b-2 border-gray-200">
      {/* Classic Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-20">
        <div className="text-center">
          {/* Logo */}
          <div className="flex justify-center mb-6">
            <div className="bg-gradient-to-br from-purple-600 to-pink-600 rounded-2xl p-6 shadow-2xl">
              <ShoppingBag className="w-20 h-20 text-white" />
            </div>
          </div>
          
          {/* Main Heading */}
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-900 mb-4">
            Welcome to C2B
          </h1>
          <p className="text-xl md:text-2xl text-gray-700 mb-3 font-semibold">
            Click to Buy - Your Trusted Online Store
          </p>
          <p className="text-lg text-gray-600 mb-8 max-w-3xl mx-auto">
            Quality products at great prices. Shop watches, gadgets, fashion, home decor, beauty products & more!
            <br />
            <span className="font-semibold text-purple-600">Fast delivery • Genuine products • Easy returns</span>
          </p>

          {/* Large Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Button
              size="lg"
              onClick={scrollToProducts}
              className="w-full sm:w-auto bg-purple-600 hover:bg-purple-700 text-white px-10 py-7 text-xl font-semibold shadow-lg hover:shadow-xl transition-all duration-200"
            >
              <ShoppingBag className="mr-3 w-6 h-6" />
              Shop Now
              <ArrowRight className="ml-3 w-6 h-6" />
            </Button>
            
            <Button
              size="lg"
              onClick={openWhatsApp}
              className="w-full sm:w-auto bg-green-600 hover:bg-green-700 text-white px-10 py-7 text-xl font-semibold shadow-lg hover:shadow-xl transition-all duration-200"
            >
              <MessageCircle className="mr-3 w-6 h-6" />
              Chat on WhatsApp
            </Button>
          </div>
        </div>
      </div>

      {/* Floating WhatsApp Button */}
      <div className="fixed bottom-6 right-6 z-50">
        <Button
          onClick={openWhatsApp}
          className="bg-green-500 hover:bg-green-600 text-white rounded-full w-16 h-16 shadow-2xl hover:scale-110 transition-transform duration-200 flex items-center justify-center"
          title="Chat on WhatsApp"
        >
          <MessageCircle className="w-8 h-8" />
        </Button>
      </div>
    </div>
  );
};

export default Hero;
