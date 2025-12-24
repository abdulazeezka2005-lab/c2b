import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { Trash2, Plus, Minus, ShoppingBag, MessageCircle, CreditCard } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import { useToast } from '../hooks/use-toast';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Cart = ({ cart, setCart }) => {
  const { toast } = useToast();
  const [paymentLoading, setPaymentLoading] = useState(false);

  const updateQuantity = (productId, change) => {
    setCart(cart.map(item =>
      item._id === productId
        ? { ...item, quantity: Math.max(1, item.quantity + change) }
        : item
    ));
  };

  const removeItem = (productId) => {
    setCart(cart.filter(item => item._id !== productId));
  };

  const totalAmount = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);

  const handleWhatsAppCheckout = async () => {
    try {
      const whatsappPhone = process.env.REACT_APP_WHATSAPP_PHONE || '1234567890';
      // Save order to backend
      const orderData = {
        items: cart.map(item => ({
          productId: item._id,
          productName: item.name,
          price: item.price,
          quantity: item.quantity
        })),
        customerPhone: whatsappPhone
      };

      const response = await axios.post(`${API}/orders`, orderData);
      
      if (response.data.order) {
        toast({
          title: "Order saved!",
          description: "Your order has been recorded. Proceed to WhatsApp.",
        });

        // Prepare WhatsApp message
        const orderDetails = cart.map(item =>
          `*${item.name}*\nQty: ${item.quantity}\nPrice: ₹${item.price} x ${item.quantity} = ₹${item.price * item.quantity}`
        ).join('\n\n');

        const message = `Hi! I want to place an order:\n\n${orderDetails}\n\n*Total: ₹${totalAmount}*\n\nOrder ID: ${response.data.order._id}\n\nPlease confirm availability and delivery details.`;
        const whatsappUrl = `https://wa.me/${whatsappPhone}?text=${encodeURIComponent(message)}`;
        window.open(whatsappUrl, '_blank');
      }
    } catch (error) {
      console.error('Error creating order:', error);
      toast({
        title: "Error",
        description: "Failed to save order. Please try again.",
        variant: "destructive"
      });
    }
  };

  if (cart.length === 0) {
    return (
      <div className="min-h-[80vh] flex items-center justify-center">
        <div className="text-center">
          <ShoppingBag className="w-24 h-24 mx-auto text-gray-300 mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Your cart is empty</h2>
          <p className="text-gray-600 mb-6">Add some products to get started!</p>
          <Link to="/">
            <Button className="bg-purple-600 hover:bg-purple-700 text-white">
              Continue Shopping
            </Button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Shopping Cart</h1>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Cart Items */}
          <div className="lg:col-span-2 space-y-4">
            {cart.map(item => (
              <Card key={item._id}>
                <CardContent className="p-4">
                  <div className="flex gap-4">
                    <img
                      src={item.image}
                      alt={item.name}
                      className="w-24 h-24 object-cover rounded-lg"
                    />
                    <div className="flex-1">
                      <h3 className="font-semibold text-lg text-gray-900">{item.name}</h3>
                      <p className="text-sm text-gray-600 mb-2">{item.description}</p>
                      <div className="flex items-center justify-between">
                        <span className="text-xl font-bold text-purple-600">₹{item.price}</span>
                        <div className="flex items-center gap-3">
                          <Button
                            size="icon"
                            variant="outline"
                            onClick={() => updateQuantity(item._id, -1)}
                            className="h-8 w-8"
                          >
                            <Minus className="w-4 h-4" />
                          </Button>
                          <span className="font-semibold w-8 text-center">{item.quantity}</span>
                          <Button
                            size="icon"
                            variant="outline"
                            onClick={() => updateQuantity(item._id, 1)}
                            className="h-8 w-8"
                          >
                            <Plus className="w-4 h-4" />
                          </Button>
                          <Button
                            size="icon"
                            variant="destructive"
                            onClick={() => removeItem(item._id)}
                            className="h-8 w-8"
                          >
                            <Trash2 className="w-4 h-4" />
                          </Button>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Order Summary */}
          <div className="lg:col-span-1">
            <Card className="sticky top-24">
              <CardContent className="p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Order Summary</h2>
                <div className="space-y-3 mb-4">
                  {cart.map(item => (
                    <div key={item._id} className="flex justify-between text-sm">
                      <span className="text-gray-600">
                        {item.name} x {item.quantity}
                      </span>
                      <span className="font-semibold">₹{item.price * item.quantity}</span>
                    </div>
                  ))}
                </div>
                <div className="border-t pt-4 mb-6">
                  <div className="flex justify-between items-center">
                    <span className="text-lg font-bold text-gray-900">Total</span>
                    <span className="text-2xl font-bold text-purple-600">₹{totalAmount}</span>
                  </div>
                </div>
                <Button
                  onClick={handleWhatsAppCheckout}
                  className="w-full bg-green-600 hover:bg-green-700 text-white py-6 text-lg"
                >
                  <MessageCircle className="w-5 h-5 mr-2" />
                  Order on WhatsApp
                </Button>
                <Link to="/">
                  <Button variant="outline" className="w-full mt-3">
                    Continue Shopping
                  </Button>
                </Link>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Cart;
