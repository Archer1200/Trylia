import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import '../styles/Header.css';

const Header = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const location = useLocation();

  // Close mobile menu when route changes
  useEffect(() => {
    setIsMobileMenuOpen(false);
  }, [location]);

  // Handle scroll effect
  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  const closeMobileMenu = () => {
    setIsMobileMenuOpen(false);
  };

  return (
    <header className={`header ${isScrolled ? 'scrolled' : ''}`}>
      <div className="container">
        <Link to="/" className="logo" onClick={closeMobileMenu}>
          <h1>Trylia</h1>
          <span className="logo-subtitle">Virtual Dressing Room</span>
        </Link>
        
        {/* Desktop Navigation */}
        <nav className="nav desktop-nav">
          <Link 
            to="/" 
            className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}
          >
            Home
          </Link>
          <Link 
            to="/about" 
            className={`nav-link ${location.pathname === '/about' ? 'active' : ''}`}
            onClick={closeMobileMenu}
          >
            About
          </Link>
          <Link 
            to="/catalog" 
            className={`nav-link ${location.pathname === '/catalog' ? 'active' : ''}`}
          >
            Try_on
          </Link>
          <a 
            href="#testimonials" 
            className="nav-link"
            onClick={closeMobileMenu}
          >
            Reviews
          </a>
          <Link 
            to="/contact" 
            className={`nav-link ${location.pathname === '/contact' ? 'active' : ''}`}
            onClick={closeMobileMenu}
          >
            Contact
          </Link>
        </nav>

        {/* Hamburger Menu Button */}
        <button 
          className={`mobile-menu-btn ${isMobileMenuOpen ? 'active' : ''}`}
          onClick={toggleMobileMenu}
          aria-label="Toggle mobile menu"
        >
          <span></span>
          <span></span>
          <span></span>
        </button>

        {/* Mobile Navigation */}
        <nav className={`mobile-nav ${isMobileMenuOpen ? 'active' : ''}`}>
          <div className="mobile-nav-content">
            <div className="mobile-nav-header">
              <h2>Navigation</h2>
              <button 
                className="close-btn"
                onClick={closeMobileMenu}
                aria-label="Close mobile menu"
              >
                ×
              </button>
            </div>
            <div className="mobile-nav-links">
              <Link 
                to="/" 
                className={`mobile-nav-link ${location.pathname === '/' ? 'active' : ''}`}
                onClick={closeMobileMenu}
              >
                <span className="nav-icon">🏠</span>
                <span className="nav-text">Home</span>
                <span className="nav-arrow">→</span>
              </Link>
              <Link 
                to="/about" 
                className={`mobile-nav-link ${location.pathname === '/about' ? 'active' : ''}`}
                onClick={closeMobileMenu}
              >
                <span className="nav-icon">ℹ️</span>
                <span className="nav-text">About</span>
                <span className="nav-arrow">→</span>
              </Link>
              <Link 
                to="/catalog" 
                className={`mobile-nav-link ${location.pathname === '/catalog' ? 'active' : ''}`}
                onClick={closeMobileMenu}
              >
                <span className="nav-icon">🛍️</span>
                <span className="nav-text">Shop</span>
                <span className="nav-arrow">→</span>
              </Link>
              <a 
                href="#testimonials" 
                className="mobile-nav-link"
                onClick={closeMobileMenu}
              >
                <span className="nav-icon">⭐</span>
                <span className="nav-text">Reviews</span>
                <span className="nav-arrow">→</span>
              </a>
              <Link 
                to="/contact" 
                className={`mobile-nav-link ${location.pathname === '/contact' ? 'active' : ''}`}
                onClick={closeMobileMenu}
              >
                <span className="nav-icon">📧</span>
                <span className="nav-text">Contact</span>
                <span className="nav-arrow">→</span>
              </Link>
            </div>
            <div className="mobile-nav-footer">
              <p>Experience fashion like never before</p>
            </div>
          </div>
        </nav>

        {/* Mobile Menu Overlay */}
        {isMobileMenuOpen && (
          <div 
            className="mobile-menu-overlay" 
            onClick={closeMobileMenu}
          ></div>
        )}
      </div>
    </header>
  );
};

export default Header;