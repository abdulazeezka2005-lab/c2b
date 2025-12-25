import React, { useState } from 'react';
import { X, ShoppingCart, CreditCard, MessageCircle } from 'lucide-react';
import { Button } from './ui/button';
import { Dialog, DialogContent } from './ui/dialog';
import { useToast } from '../hooks/use-toast';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ProductDetailModal = ({ product, isOpen, onClose, onAddToCart }) => {
  const { toast } = useToast();
  const [paymentLoading, setPaymentLoading] = useState(false);
  const [quantity, setQuantity] = useState(1);

  if (!product) return null;

  const getImageUrl = (imageUrl) => {
    if (!imageUrl) return 'https://via.placeholder.com/400';
    if (imageUrl.startsWith('http')) return imageUrl;
    if (imageUrl.startsWith('/api/')) return `${BACKEND_URL}${imageUrl}`;
    return imageUrl;
  };

  const totalPrice = product.price * quantity;

  const handleDirectPayment = async () => {
    setPaymentLoading(true);
    try {
      // Create order
      const orderData = {
        items: [{
          productId: product._id,
          productName: product.name,
          price: product.price,
          quantity: quantity
        }],
        customerPhone: "6380832058"
      };

      const orderResponse = await axios.post(`${API}/orders`, orderData);
      const orderId = orderResponse.data.order._id;

      // Get Razorpay config
      const configResponse = await axios.get(`${API}/payments/config`);
      const razorpayKey = configResponse.data.key;

      // Create Razorpay order
      const paymentOrderResponse = await axios.post(`${API}/payments/create-order`, {
        amount: totalPrice * 100,
        currency: "INR",
        orderId: orderId
      });

      // Initialize Razorpay
      const options = {
        key: razorpayKey,
        amount: paymentOrderResponse.data.amount,
        currency: paymentOrderResponse.data.currency,
        order_id: paymentOrderResponse.data.orderId,
        name: "C2B - Click to Buy",
        description: product.name,
        image: getImageUrl(product.image),
        handler: async function (response) {
          try {
            await axios.post(`${API}/payments/verify`, {
              razorpay_order_id: response.razorpay_order_id,
              razorpay_payment_id: response.razorpay_payment_id,
              razorpay_signature: response.razorpay_signature
            });

            toast({
              title: "Payment Successful!",
              description: "Your order has been placed. We'll contact you soon!",
            });

            onClose();
          } catch (error) {
            toast({
              title: "Payment Verification Failed",
              description: "Please contact support.",
              variant: "destructive"
            });
          }
        },
        prefill: {
          contact: "6380832058"
        },
        theme: {
          color: "#9333EA"
        },
        modal: {
          ondismiss: function() {
            setPaymentLoading(false);
          }
        }
      };

      if (window.Razorpay) {
        const razorpay = new window.Razorpay(options);
        razorpay.open();
      }
    } catch (error) {
      console.error('Payment error:', error);
      toast({
        title: "Payment Failed",
        description: "Unable to process payment. Please try again.",
        variant: "destructive"
      });
    } finally {
      setPaymentLoading(false);
    }
  };

  const handleWhatsAppOrder = () => {
    const whatsappPhone = process.env.REACT_APP_WHATSAPP_PHONE || '916380832058';
    const message = `Hi! I want to buy:

*${product.name}*
Quantity: ${quantity}
Price: ₹${product.price} x ${quantity} = ₹${totalPrice}

Please confirm availability.`;
    const whatsappUrl = `https://wa.me/${whatsappPhone}?text=${encodeURIComponent(message)}`;
    window.open(whatsappUrl, '_blank');
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto p-0">
        <div className="relative">
          <button
            onClick={onClose}
            className="absolute top-4 right-4 z-10 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100"
          >
            <X className="w-5 h-5" />
          </button>

          <div className="grid md:grid-cols-2 gap-6 p-6">
            {/* Product Image */}
            <div className="space-y-4">
              <img
                src={getImageUrl(product.image)}
                alt={product.name}
                className="w-full h-96 object-cover rounded-lg"
                onError={(e) => {
                  e.target.src = 'https://via.placeholder.com/400?text=Product+Image';
                }}
              />
            </div>

            {/* Product Details */}
            <div className="space-y-4">
              <div>
                <h2 className="text-3xl font-bold text-gray-900 mb-2">{product.name}</h2>
                <p className="text-gray-600">{product.description}</p>
              </div>

              <div className="border-t border-b py-4 space-y-2">
                <div className="flex items-baseline gap-3">
                  <span className="text-4xl font-bold text-purple-600">₹{product.price}</span>
                  <span className="text-lg text-gray-500 line-through">₹{Math.round(product.price * 1.3)}</span>
                </div>
                <p className="text-sm text-green-600 font-semibold">Save {Math.round(((product.price * 1.3 - product.price) / (product.price * 1.3)) * 100)}% off</p>
                {product.inStock ? (
                  <p className="text-green-600 font-semibold flex items-center gap-2">
                    <span className="w-2 h-2 bg-green-600 rounded-full"></span>
                    In Stock - Ready to Ship
                  </p>
                ) : (
                  <p className="text-red-600 font-semibold">Out of Stock</p>
                )}
              </div>

              {/* Quantity Selector */}
              <div className="space-y-2">
                <label className="text-sm font-semibold text-gray-700">Quantity:</label>
                <div className="flex items-center gap-3">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setQuantity(Math.max(1, quantity - 1))}
                    disabled={!product.inStock}
                  >
                    -
                  </Button>
                  <span className="text-xl font-bold w-12 text-center">{quantity}</span>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setQuantity(quantity + 1)}
                    disabled={!product.inStock}
                  >
                    +
                  </Button>
                </div>
              </div>

              {/* Total Price */}
              <div className="bg-purple-50 p-4 rounded-lg border-2 border-purple-200">
                <div className="flex justify-between items-center">
                  <span className="text-lg font-semibold text-gray-700">Total Amount:</span>
                  <span className="text-3xl font-bold text-purple-600">₹{totalPrice}</span>
                </div>
              </div>

              {/* Payment Info */}
              <div className="bg-green-50 p-3 rounded-lg border border-green-200">
                <p className="text-sm text-green-800 font-semibold">
                  🎉 0% Payment Fee on RuPay & UPI
                </p>
                <p className="text-xs text-green-700 mt-1">
                  Pay with UPI or RuPay cards - No extra charges!
                </p>
              </div>

              {/* Action Buttons */}
              <div className="space-y-3 pt-2">
                <Button
                  onClick={handleDirectPayment}
                  disabled={!product.inStock || paymentLoading}
                  className="w-full bg-purple-600 hover:bg-purple-700 text-white py-6 text-lg font-semibold"
                >
                  <CreditCard className="w-5 h-5 mr-2" />
                  {paymentLoading ? 'Processing...' : 'Buy Now - Pay Securely'}
                </Button>

                <Button
                  onClick={() => {
                    onAddToCart(product, quantity);
                    toast({
                      title: "Added to cart!",
                      description: `${quantity}x ${product.name} added to cart.`,
                    });
                  }}
                  disabled={!product.inStock}
                  variant="outline"
                  className="w-full py-6 text-lg font-semibold border-2 border-purple-600 text-purple-600 hover:bg-purple-50"
                >
                  <ShoppingCart className="w-5 h-5 mr-2" />
                  Add to Cart
                </Button>

                <Button
                  onClick={handleWhatsAppOrder}
                  disabled={!product.inStock}
                  variant="outline"
                  className="w-full py-6 text-lg font-semibold border-2 border-green-600 text-green-600 hover:bg-green-50"
                >
                  <MessageCircle className="w-5 h-5 mr-2" />
                  Order via WhatsApp
                </Button>
              </div>

              {/* Trust Badges */}
              <div className="grid grid-cols-3 gap-2 pt-4 border-t">
                <div className="text-center">
                  <div className="text-2xl mb-1">🔒</div>
                  <p className="text-xs text-gray-600 font-semibold">Secure Payment</p>
                </div>
                <div className="text-center">
                  <div className="text-2xl mb-1">✓</div>
                  <p className="text-xs text-gray-600 font-semibold">Genuine Product</p>
                </div>
                <div className="text-center">
                  <div className="text-2xl mb-1">🚚</div>
                  <p className="text-xs text-gray-600 font-semibold">Fast Delivery</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default ProductDetailModal;