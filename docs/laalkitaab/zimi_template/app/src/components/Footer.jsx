import React from 'react';
import { Link } from 'react-router-dom';
import { Star, Mail, Phone, MapPin } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-10 h-10 bg-gradient-to-r from-orange-500 to-red-500 rounded-full flex items-center justify-center">
                <Star className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="text-lg font-bold">लाल किताब कुंडली</h3>
                <p className="text-xs text-gray-400">Lal Kitab Kundli</p>
              </div>
            </div>
            <p className="text-gray-400 text-sm">
              Discover the ancient wisdom of Lal Kitab astrology. Get accurate predictions and effective remedies for all aspects of life.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2 text-gray-400">
              <li><Link to="/" className="hover:text-orange-400 transition-colors">Home</Link></li>
              <li><Link to="/about" className="hover:text-orange-400 transition-colors">About Us</Link></li>
              <li><Link to="/features" className="hover:text-orange-400 transition-colors">Features</Link></li>
              <li><Link to="/create-kundli" className="hover:text-orange-400 transition-colors">Create Kundli</Link></li>
              <li><Link to="/dashboard" className="hover:text-orange-400 transition-colors">My Kundlis</Link></li>
            </ul>
          </div>

          {/* Services */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Our Services</h4>
            <ul className="space-y-2 text-gray-400">
              <li>Kundli Generation</li>
              <li>Marriage Predictions</li>
              <li>Career Guidance</li>
              <li>Health Analysis</li>
              <li>Wealth Predictions</li>
              <li>Lal Kitab Remedies</li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Contact Us</h4>
            <ul className="space-y-3 text-gray-400">
              <li className="flex items-center space-x-2">
                <Mail className="w-5 h-5 text-orange-500" />
                <span>support@lalkitabkundli.com</span>
              </li>
              <li className="flex items-center space-x-2">
                <Phone className="w-5 h-5 text-orange-500" />
                <span>+91 98765 43210</span>
              </li>
              <li className="flex items-center space-x-2">
                <MapPin className="w-5 h-5 text-orange-500" />
                <span>New Delhi, India</span>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; 2024 Lal Kitab Kundli. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
