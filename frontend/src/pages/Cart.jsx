import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { Trash2, Plus, Minus, ShoppingBag, MessageCircle, Smartphone, Building2, Banknote, Copy, CreditCard } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '../components/ui/dialog';
import { useToast } from '../hooks/use-toast';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Cart = ({ cart, setCart }) => {
  const { toast } = useToast();
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [selectedPayment, setSelectedPayment] = useState(null);
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
      const whatsappPhone = process.env.REACT_APP_WHATSAPP_PHONE || '916380832058';
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

  const handlePaymentMethodSelect = (method) => {
    setSelectedPayment(method);
    setShowPaymentModal(true);
  };

  const copyToClipboard = (text, label) => {
    navigator.clipboard.writeText(text);
    toast({
      title: "Copied!",
      description: `${label} copied to clipboard`,
    });
  };

  const handleConfirmPayment = async () => {
    try {
      // Save order to backend
      const orderData = {
        items: cart.map(item => ({
          productId: item._id,
          productName: item.name,
          price: item.price,
          quantity: item.quantity
        })),
        customerPhone: "6380832058"
      };

      const response = await axios.post(`${API}/orders`, orderData);
      
      if (response.data.order) {
        toast({
          title: "Order Placed!",
          description: `Your order ID: ${response.data.order._id}. We'll confirm once payment is received.`,
        });

        // Send confirmation via WhatsApp
        const whatsappPhone = process.env.REACT_APP_WHATSAPP_PHONE || '916380832058';
        const orderDetails = cart.map(item =>
          `${item.name} x ${item.quantity} = ₹${item.price * item.quantity}`
        ).join('\n');
        
        const message = `New Order Placed!\n\nOrder ID: ${response.data.order._id}\nPayment Method: ${selectedPayment}\n\n${orderDetails}\n\nTotal: ₹${totalAmount}\n\nWaiting for payment confirmation.`;
        const whatsappUrl = `https://wa.me/${whatsappPhone}?text=${encodeURIComponent(message)}`;
        window.open(whatsappUrl, '_blank');

        // Clear cart after order
        setCart([]);
        setShowPaymentModal(false);
      }
    } catch (error) {
      console.error('Error creating order:', error);
      toast({
        title: "Error",
        description: "Failed to place order. Please try again.",
        variant: "destructive"
      });
    }
  };

  const handleRazorpayPayment = async () => {
    setPaymentLoading(true);
    try {
      // Create order in database first
      const orderData = {
        items: cart.map(item => ({
          productId: item._id,
          productName: item.name,
          price: item.price,
          quantity: item.quantity
        })),
        customerPhone: "6380832058"
      };

      const orderResponse = await axios.post(`${API}/orders`, orderData);
      const orderId = orderResponse.data.order._id;

      // Get Razorpay config
      const configResponse = await axios.get(`${API}/payments/config`);
      const razorpayKey = configResponse.data.key;

      // Create Razorpay order
      const paymentOrderResponse = await axios.post(`${API}/payments/create-order`, {
        amount: totalAmount * 100, // Convert to paise
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
        description: "Product Purchase",
        image: "https://via.placeholder.com/150?text=C2B",
        handler: async function (response) {
          try {
            // Verify payment
            await axios.post(`${API}/payments/verify`, {
              razorpay_order_id: response.razorpay_order_id,
              razorpay_payment_id: response.razorpay_payment_id,
              razorpay_signature: response.razorpay_signature
            });

            toast({
              title: "Payment Successful!",
              description: "Your order has been placed successfully.",
            });

            // Clear cart
            setCart([]);
          } catch (error) {
            toast({
              title: "Payment Verification Failed",
              description: "Please contact support with your payment details.",
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
            toast({
              title: "Payment Cancelled",
              description: "You can try again or use other payment methods.",
            });
          }
        }
      };

      if (window.Razorpay) {
        const razorpay = new window.Razorpay(options);
        razorpay.open();
      } else {
        throw new Error("Razorpay SDK not loaded");
      }
    } catch (error) {
      console.error('Payment error:', error);
      toast({
        title: "Payment Failed",
        description: error.response?.data?.detail || "Unable to process payment. Try other payment methods.",
        variant: "destructive"
      });
    } finally {
      setPaymentLoading(false);
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
                
                {/* Payment Options */}
                <div className="space-y-3 mb-4">
                  <p className="text-sm font-semibold text-gray-700">Choose Payment Method:</p>
                  
                  <Button
                    onClick={() => handlePaymentMethodSelect('UPI')}
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white py-5 text-base justify-start"
                  >
                    <Smartphone className="w-5 h-5 mr-3" />
                    Pay via UPI (Google Pay/PhonePe/Paytm)
                  </Button>
                  
                  <Button
                    onClick={() => handlePaymentMethodSelect('Bank Transfer')}
                    variant="outline"
                    className="w-full py-5 text-base justify-start border-2 hover:bg-gray-50"
                  >
                    <Building2 className="w-5 h-5 mr-3" />
                    Bank Transfer / NEFT / IMPS
                  </Button>
                  
                  <Button
                    onClick={() => handlePaymentMethodSelect('Cash on Delivery')}
                    variant="outline"
                    className="w-full py-5 text-base justify-start border-2 hover:bg-gray-50"
                  >
                    <Banknote className="w-5 h-5 mr-3" />
                    Cash on Delivery (COD)
                  </Button>
                </div>

                <div className="border-t pt-3">
                  <Button
                    onClick={handleWhatsAppCheckout}
                    className="w-full bg-green-600 hover:bg-green-700 text-white py-5 text-base"
                  >
                    <MessageCircle className="w-5 h-5 mr-2" />
                    Order via WhatsApp
                  </Button>
                </div>
                
                <Link to="/">
                  <Button variant="outline" className="w-full mt-3">
                    Continue Shopping
                  </Button>
                </Link>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Payment Details Modal */}
        <Dialog open={showPaymentModal} onOpenChange={setShowPaymentModal}>
          <DialogContent className="max-w-md">
            <DialogHeader>
              <DialogTitle className="text-xl font-bold">
                {selectedPayment} Payment Details
              </DialogTitle>
            </DialogHeader>
            
            <div className="space-y-4 mt-4">
              {selectedPayment === 'UPI' && (
                <div className="space-y-3">
                  <p className="text-sm text-gray-600">Pay ₹{totalAmount} to our UPI ID:</p>
                  <div className="bg-blue-50 p-4 rounded-lg border-2 border-blue-200">
                    <div className="flex justify-between items-center">
                      <span className="text-lg font-bold text-blue-900">
                        {process.env.REACT_APP_UPI_ID || '6380832058@paytm'}
                      </span>
                      <Button
                        size="sm"
                        onClick={() => copyToClipboard(process.env.REACT_APP_UPI_ID || '6380832058@paytm', 'UPI ID')}
                      >
                        <Copy className="w-4 h-4 mr-1" />
                        Copy
                      </Button>
                    </div>
                  </div>
                  <div className="bg-yellow-50 p-3 rounded border border-yellow-200">
                    <p className="text-sm text-yellow-800">
                      <strong>Steps:</strong>
                      <br />1. Open your UPI app (GPay/PhonePe/Paytm)
                      <br />2. Send ₹{totalAmount} to above UPI ID
                      <br />3. Take screenshot of payment
                      <br />4. Click "Confirm Payment" below
                    </p>
                  </div>
                </div>
              )}

              {selectedPayment === 'Bank Transfer' && (
                <div className="space-y-3">
                  <p className="text-sm text-gray-600">Transfer ₹{totalAmount} to:</p>
                  <div className="bg-gray-50 p-4 rounded-lg border space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Bank Name:</span>
                      <span className="font-semibold">{process.env.REACT_APP_BANK_NAME || 'State Bank of India'}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Account Number:</span>
                      <div className="flex items-center gap-2">
                        <span className="font-semibold">{process.env.REACT_APP_ACCOUNT_NUMBER || '1234567890'}</span>
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => copyToClipboard(process.env.REACT_APP_ACCOUNT_NUMBER || '1234567890', 'Account Number')}
                        >
                          <Copy className="w-3 h-3" />
                        </Button>
                      </div>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">IFSC Code:</span>
                      <div className="flex items-center gap-2">
                        <span className="font-semibold">{process.env.REACT_APP_IFSC_CODE || 'SBIN0001234'}</span>
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => copyToClipboard(process.env.REACT_APP_IFSC_CODE || 'SBIN0001234', 'IFSC Code')}
                        >
                          <Copy className="w-3 h-3" />
                        </Button>
                      </div>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600">Account Holder:</span>
                      <span className="font-semibold">C2B Store</span>
                    </div>
                  </div>
                </div>
              )}

              {selectedPayment === 'Cash on Delivery' && (
                <div className="space-y-3">
                  <div className="bg-green-50 p-4 rounded-lg border border-green-200">
                    <p className="text-green-800">
                      <strong>Cash on Delivery Available!</strong>
                    </p>
                    <p className="text-sm text-green-700 mt-2">
                      Pay ₹{totalAmount} in cash when you receive your order. No advance payment needed!
                    </p>
                  </div>
                  <div className="bg-gray-50 p-3 rounded">
                    <p className="text-sm text-gray-700">
                      <strong>Note:</strong> COD orders will be confirmed via WhatsApp. Please keep ₹{totalAmount} ready at the time of delivery.
                    </p>
                  </div>
                </div>
              )}

              <Button
                onClick={handleConfirmPayment}
                className="w-full bg-purple-600 hover:bg-purple-700 text-white py-6 text-lg"
              >
                Confirm & Place Order
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>
    </div>
  );
};

export default Cart;
