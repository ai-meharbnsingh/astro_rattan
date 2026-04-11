import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Menu, X, User, LogOut, Star } from 'lucide-react';

const Header = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header className="bg-gradient-to-r from-orange-600 via-red-600 to-pink-600 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center">
              <Star className="w-6 h-6 text-orange-600" />
            </div>
            <div>
              <h1 className="text-xl font-bold">लाल किताब कुंडली</h1>
              <p className="text-xs text-orange-100">Lal Kitab Kundli</p>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-6">
            <Link to="/" className="hover:text-orange-200 transition-colors">Home</Link>
            <Link to="/about" className="hover:text-orange-200 transition-colors">About</Link>
            <Link to="/features" className="hover:text-orange-200 transition-colors">Features</Link>
            {user ? (
              <>
                <Link to="/dashboard" className="hover:text-orange-200 transition-colors">Dashboard</Link>
                <Link to="/create-kundli" className="bg-white text-orange-600 px-4 py-2 rounded-full font-medium hover:bg-orange-100 transition-colors">
                  Create Kundli
                </Link>
                <div className="flex items-center space-x-2">
                  <User className="w-5 h-5" />
                  <span>{user.name}</span>
                </div>
                <button onClick={handleLogout} className="flex items-center space-x-1 hover:text-orange-200">
                  <LogOut className="w-5 h-5" />
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="hover:text-orange-200 transition-colors">Login</Link>
                <Link to="/register" className="bg-white text-orange-600 px-4 py-2 rounded-full font-medium hover:bg-orange-100 transition-colors">
                  Register
                </Link>
              </>
            )}
          </nav>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden p-2"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t border-orange-500">
            <nav className="flex flex-col space-y-4">
              <Link to="/" className="hover:text-orange-200" onClick={() => setIsMenuOpen(false)}>Home</Link>
              <Link to="/about" className="hover:text-orange-200" onClick={() => setIsMenuOpen(false)}>About</Link>
              <Link to="/features" className="hover:text-orange-200" onClick={() => setIsMenuOpen(false)}>Features</Link>
              {user ? (
                <>
                  <Link to="/dashboard" className="hover:text-orange-200" onClick={() => setIsMenuOpen(false)}>Dashboard</Link>
                  <Link to="/create-kundli" className="hover:text-orange-200" onClick={() => setIsMenuOpen(false)}>Create Kundli</Link>
                  <button onClick={() => { handleLogout(); setIsMenuOpen(false); }} className="text-left hover:text-orange-200">
                    Logout
                  </button>
                </>
              ) : (
                <>
                  <Link to="/login" className="hover:text-orange-200" onClick={() => setIsMenuOpen(false)}>Login</Link>
                  <Link to="/register" className="hover:text-orange-200" onClick={() => setIsMenuOpen(false)}>Register</Link>
                </>
              )}
            </nav>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;
