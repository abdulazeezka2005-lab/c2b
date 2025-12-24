import { useState } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import Cart from "./pages/Cart";
import AdminLogin from "./pages/AdminLogin";
import AdminDashboard from "./pages/AdminDashboard";
import { Toaster } from "./components/ui/sonner";
import { AdminProvider } from "./context/AdminContext";
import { categories } from "./mock";

function App() {
  const [cart, setCart] = useState([]);

  return (
    <div className="App">
      <BrowserRouter>
        <AdminProvider>
          <Routes>
            {/* Public Routes */}
            <Route path="/" element={
              <>
                <Navbar cartCount={cart.reduce((sum, item) => sum + item.quantity, 0)} categories={categories} />
                <Home cart={cart} setCart={setCart} />
                <Footer />
              </>
            } />
            <Route path="/cart" element={
              <>
                <Navbar cartCount={cart.reduce((sum, item) => sum + item.quantity, 0)} categories={categories} />
                <Cart cart={cart} setCart={setCart} />
                <Footer />
              </>
            } />
            
            {/* Admin Routes */}
            <Route path="/admin/login" element={<AdminLogin />} />
            <Route path="/admin/dashboard" element={<AdminDashboard />} />
          </Routes>
          <Toaster />
        </AdminProvider>
      </BrowserRouter>
    </div>
  );
}

export default App;
