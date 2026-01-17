import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import About from '../components/sections/About';
import Testimonials from '../components/sections/Testimonials';
import '../styles/Home.css';

const Home = () => {
  const [isVideoPlaying, setIsVideoPlaying] = useState(true); // Start as true since autoplay is enabled

  const handleVideoPlay = () => {
    setIsVideoPlaying(true);
  };

  const handleVideoPause = () => {
    setIsVideoPlaying(false);
  };

  return (
    <div className="home">
      <section className="hero">
        <div className="container">
          <div className="hero-content">
            <h1 className="hero-title">Trylia</h1>
            <p className="hero-tagline">Your Virtual Dressing Room</p>
            <p className="hero-description">
              Experience fashion like never before. Try on clothes virtually and find your perfect style.
            </p>
            <Link to="/catalog" className="cta-button">
              Try_on
            </Link>
          </div>
          <div className="hero-video">
            <div className={`video-card ${isVideoPlaying ? 'playing' : ''}`}>
              <div className="video-card-header">
                <h3 className="video-card-title">Virtual Dressing Room</h3>
                <div className="video-card-subtitle">See it in action</div>
              </div>
              <div className="video-container">
                <video 
                  className="demo-video"
                  controls
                  autoPlay
                  muted
                  loop
                  poster="/images/video-poster.jpg"
                  onPlay={handleVideoPlay}
                  onPause={handleVideoPause}
                  onEnded={handleVideoPause}
                >
                  <source src="/videos/demo.mp4" type="video/mp4" />
                  Your browser does not support the video tag.
                </video>
                {!isVideoPlaying && (
                  <div className="video-overlay">
                    <div className="play-button">
                      <svg width="60" height="60" viewBox="0 0 60 60" fill="none">
                        <circle cx="30" cy="30" r="30" fill="rgba(220, 38, 38, 0.9)" />
                        <path d="M23 20L40 30L23 40V20Z" fill="white" />
                      </svg>
                    </div>
                  </div>
                )}
              </div>
              <div className="video-card-footer">
                <span className="video-duration">Live Demo</span>
                <div className="video-stats">
                  <span className="stat-item">🎥 HD Quality</span>
                  <span className="stat-item">⚡ Auto-play</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
      
      <section className="features">
        <div className="container">
          <h2>Why Choose Trylia?</h2>
          <div className="features-grid">
            <div className="feature">
              <div className="feature-icon">👗</div>
              <h3>Virtual Try-On</h3>
              <p>See how clothes look on you before buying with our advanced AR technology</p>
            </div>
            <div className="feature">
              <div className="feature-icon">✨</div>
              <h3>Quality Fashion</h3>
              <p>Curated collection of premium clothing from top brands</p>
            </div>
            {/* <div className="feature">
              <div className="feature-icon">🚚</div>
              <h3>Fast Delivery</h3>
              <p>Quick and reliable shipping worldwide with real-time tracking</p>
            </div> */}
          </div>
        </div>
      </section>
      
      {/* <About /> */}
      <Testimonials />
    </div>
  );
};

export default Home;