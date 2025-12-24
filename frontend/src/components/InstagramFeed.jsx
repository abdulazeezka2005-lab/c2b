import React from 'react';
import { Instagram, Heart, MessageCircle } from 'lucide-react';
import { Button } from './ui/button';

const InstagramFeed = ({ posts }) => {
  const instagramUrl = process.env.REACT_APP_INSTAGRAM_URL || 'https://instagram.com';
  
  return (
    <div className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-4">
            <Instagram className="w-8 h-8 text-pink-600 mr-2" />
            <h2 className="text-3xl font-bold text-gray-900">Follow Us on Instagram</h2>
          </div>
          <p className="text-gray-600 mb-6">Stay updated with our latest products and offers</p>
          <a
            href={instagramUrl}
            target="_blank"
            rel="noopener noreferrer"
          >
            <Button className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white">
              <Instagram className="w-5 h-5 mr-2" />
              Follow @stylehub
            </Button>
          </a>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-2">
          {posts.map(post => (
            <div
              key={post.id}
              className="relative group overflow-hidden aspect-square cursor-pointer rounded-lg"
            >
              <img
                src={post.image}
                alt="Instagram post"
                className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
              />
              <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-50 transition-all duration-300 flex items-center justify-center">
                <div className="opacity-0 group-hover:opacity-100 transition-opacity duration-300 text-white flex items-center space-x-4">
                  <div className="flex items-center">
                    <Heart className="w-6 h-6 mr-1" />
                    <span className="font-semibold">{post.likes}</span>
                  </div>
                  <div className="flex items-center">
                    <MessageCircle className="w-6 h-6 mr-1" />
                    <span className="font-semibold">{post.comments}</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default InstagramFeed;
