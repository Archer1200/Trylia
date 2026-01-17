import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Footer.css';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer" id="contact">
      <div className="footer-content">
        <div className="container">
          <div className="footer-grid">
            {/* Brand Section */}
            <div className="footer-section brand-section">
              <div className="footer-logo">
                <h3>Trylia</h3>
                <span className="footer-tagline">Virtual Dressing Room</span>
              </div>
              <p className="footer-description">
                Experience fashion like never before with our cutting-edge virtual try-on technology. 
                Shop with confidence and find your perfect style.
              </p>
              <div className="social-links">
                <a href="#" className="social-link" aria-label="Facebook">
                  <span className="social-icon">📘</span>
                </a>
                <a href="#" className="social-link" aria-label="Instagram">
                  <span className="social-icon">📷</span>
                </a>
                <a href="#" className="social-link" aria-label="Twitter">
                  <span className="social-icon">🐦</span>
                </a>
                <a href="#" className="social-link" aria-label="LinkedIn">
                  <span className="social-icon">💼</span>
                </a>
                <a href="#" className="social-link" aria-label="YouTube">
                  <span className="social-icon">📺</span>
                </a>
              </div>
            </div>

            {/* Quick Links */}
            <div className="footer-section">
              <h4 className="footer-title">Quick Links</h4>
              <ul className="footer-links">
                <li><Link to="/">Home</Link></li>
                <li><Link to="/catalog">Shop</Link></li>
                <li><Link to="/about">About Us</Link></li>
                <li><a href="#testimonials">Reviews</a></li>
                <li><a href="#contact">Contact</a></li>
              </ul>
            </div>

            {/* Categories */}
            <div className="footer-section">
              <h4 className="footer-title">Categories</h4>
              <ul className="footer-links">
                <li><a href="#">Men's Fashion</a></li>
                <li><a href="#">Women's Fashion</a></li>
                <li><a href="#">New Arrivals</a></li>
              </ul>
            </div>

            {/* Support */}
            <div className="footer-section">
              <h4 className="footer-title">Support</h4>
              <ul className="footer-links">
                <li><a href="#">Help Center</a></li>
                <li><a href="#">Returns & Exchanges</a></li>
                <li><a href="#">Shipping Info</a></li>
                <li><a href="#">Track Your Order</a></li>
              </ul>
            </div>

            {/* Newsletter */}
            {/* <div className="footer-section newsletter-section">
              <h4 className="footer-title">Stay Updated</h4>
              <p className="newsletter-description">
                Subscribe to get special offers, free giveaways, and updates on new features.
              </p>
              <form className="newsletter-form">
                <div className="input-group">
                  <input 
                    type="email" 
                    placeholder="Enter your email"
                    className="newsletter-input"
                    required
                  />
                  <button type="submit" className="newsletter-btn">
                    Subscribe
                  </button>
                </div>
              </form>
              <div className="newsletter-features">
                <div className="feature-item">
                  <span className="feature-icon">🎁</span>
                  <span>Exclusive Offers</span>
                </div>
                <div className="feature-item">
                  <span className="feature-icon">🚀</span>
                  <span>Early Access</span>
                </div>
              </div>
            </div> */}
          </div>
        </div>
      </div>

      {/* Footer Bottom */}
      <div className="footer-bottom">
        <div className="container">
          <div className="footer-bottom-content">
            <div className="footer-bottom-left">
              <p>&copy; {currentYear} Trylia. All rights reserved.</p>
              <div className="footer-bottom-links">
                <a href="#">Privacy Policy</a>
                <a href="#">Terms of Service</a>
                <a href="#">Cookie Policy</a>
              </div>
            </div>
            <div className="footer-bottom-right">
              <div className="payment-methods">
                <span className="payment-label">We Accept:</span>
                <div className="payment-icons">
                  <span className="payment-icon">💳</span>
                  <span className="payment-icon">🏦</span>
                  <span className="payment-icon">📱</span>
                  <span className="payment-icon">💰</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Floating Elements */}
      <div className="footer-decoration">
        <div className="floating-element element-1"></div>
        <div className="floating-element element-2"></div>
        <div className="floating-element element-3"></div>
      </div>
    </footer>
  );
};

export default Footer;