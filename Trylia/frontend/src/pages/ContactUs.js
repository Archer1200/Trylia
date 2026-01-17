import React from 'react';
import ContactForm from '../components/ContactUs/ContactForm';
import './ContactUs.css';

const ContactUs = () => {
  return (
    <div className="contact-us-page">
      <div className="page-container">
        {/* Hero Section */}
        <section className="contact-hero">
          <div className="hero-content">
            <h1>Partner with Trylia</h1>
            <p className="hero-subtitle">
              Transform your e-commerce platform with cutting-edge virtual try-on technology. 
              Join leading retailers who are revolutionizing online shopping experiences.
            </p>
            <div className="hero-stats">
              <div className="stat">
                <span className="stat-number">95%</span>
                <span className="stat-label">Customer Satisfaction</span>
              </div>
              <div className="stat">
                <span className="stat-number">40%</span>
                <span className="stat-label">Reduced Returns</span>
              </div>
              <div className="stat">
                <span className="stat-number">60%</span>
                <span className="stat-label">Increased Conversions</span>
              </div>
            </div>
          </div>
        </section>

        {/* Benefits Section */}
        <section className="benefits-section">
          <div className="benefits-grid">
            <div className="benefit-card">
              <div className="benefit-icon">🚀</div>
              <h3>Quick Integration</h3>
              <p>Seamless API integration with your existing e-commerce platform in just days, not months.</p>
            </div>
            <div className="benefit-card">
              <div className="benefit-icon">🎯</div>
              <h3>Accurate Sizing</h3>
              <p>AI-powered size recommendations reduce returns and increase customer confidence.</p>
            </div>
            <div className="benefit-card">
              <div className="benefit-icon">📱</div>
              <h3>Mobile Optimized</h3>
              <p>Perfect performance across all devices with responsive design and fast loading.</p>
            </div>
            <div className="benefit-card">
              <div className="benefit-icon">🔧</div>
              <h3>Custom Solutions</h3>
              <p>Tailored implementations to match your brand and specific business requirements.</p>
            </div>
          </div>
        </section>

        {/* Contact Form Section */}
        <section className="contact-form-section">
          <ContactForm />
        </section>

        {/* Additional Info Section */}
        <section className="additional-info">
          <div className="info-grid">
            <div className="info-card">
              <h3>🕐 Response Time</h3>
              <p>We respond to all inquiries within 24 hours during business days. For urgent requests, please mention it in your message.</p>
            </div>
            <div className="info-card">
              <h3>🎥 Demo Available</h3>
              <p>Schedule a personalized demo to see Trylia in action with your products and understand the integration process.</p>
            </div>
            <div className="info-card">
              <h3>💼 Enterprise Support</h3>
              <p>Dedicated account management and technical support for enterprise clients with custom SLAs.</p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default ContactUs;