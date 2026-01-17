import React from 'react';
import '../../styles/About.css';

const About = () => {
  return (
    <section className="about" id="about">
      <div className="container">
        <div className="about-content">
          <div className="about-text">
            <h2 className="about-title">About Trylia</h2>
            <p className="about-subtitle">Revolutionizing Fashion with Technology</p>
            <div className="about-description">
              <p>
                At Trylia, we believe that shopping for clothes should be an exciting, 
                confident, and personalized experience. Our cutting-edge virtual try-on 
                technology combines artificial intelligence with augmented reality to 
                bring the fitting room directly to your device.
              </p>
              <p>
                Founded in 2024, we've partnered with leading fashion brands to create 
                an immersive shopping experience that eliminates the guesswork from 
                online clothing purchases. Our mission is to make fashion accessible, 
                sustainable, and perfectly fitted for everyone.
              </p>
            </div>
            <div className="about-stats">
              <div className="stat">
                <div className="stat-number">50K+</div>
                <div className="stat-label">Happy Customers</div>
              </div>
              <div className="stat">
                <div className="stat-number">1M+</div>
                <div className="stat-label">Virtual Try-Ons</div>
              </div>
              <div className="stat">
                <div className="stat-number">500+</div>
                <div className="stat-label">Brand Partners</div>
              </div>
            </div>
          </div>
          <div className="about-visual">
            <div className="about-card">
              <div className="card-header">
                <h3>Our Technology</h3>
                <div className="tech-badge">AI Powered</div>
              </div>
              <div className="tech-features">
                <div className="tech-feature">
                  <div className="tech-icon">🤖</div>
                  <div className="tech-info">
                    <h4>AI Body Mapping</h4>
                    <p>Advanced algorithms analyze your body measurements</p>
                  </div>
                </div>
                <div className="tech-feature">
                  <div className="tech-icon">📱</div>
                  <div className="tech-info">
                    <h4>AR Integration</h4>
                    <p>Real-time augmented reality clothing visualization</p>
                  </div>
                </div>
                <div className="tech-feature">
                  <div className="tech-icon">🎯</div>
                  <div className="tech-info">
                    <h4>Perfect Fit</h4>
                    <p>99% accuracy in size recommendations</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;