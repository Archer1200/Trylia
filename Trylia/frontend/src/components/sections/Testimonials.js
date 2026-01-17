import React, { useState, useEffect } from 'react';
import '../../styles/Testimonials.css';
import '../../styles/TestimonialsEnhanced.css';

const Testimonials = () => {
  const [currentTestimonial, setCurrentTestimonial] = useState(0);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [showVideoTestimonials, setShowVideoTestimonials] = useState(false);

  const testimonials = [
    {
      id: 1,
      name: "Sarah Johnson",
      role: "Fashion Enthusiast",
      avatar: "👩‍💼",
      rating: 5,
      text: "Trylia completely changed how I shop online! The virtual try-on feature is incredibly accurate. I haven't had a single return since I started using it.",
      location: "New York, USA",
      category: "fashion",
      verified: true,
      purchaseCount: 15,
      favoriteFeature: "Virtual Try-On"
    },
    {
      id: 2,
      name: "Michael Chen",
      role: "Tech Professional",
      avatar: "👨‍💻",
      rating: 5,
      text: "As someone who hates shopping in stores, Trylia is a game-changer. The AR technology is so realistic, I can see exactly how clothes will look on me.",
      location: "San Francisco, USA",
      category: "technology",
      verified: true,
      purchaseCount: 8,
      favoriteFeature: "AR Technology"
    },
    {
      id: 3,
      name: "Emma Rodriguez",
      role: "Style Blogger",
      avatar: "👩‍🎨",
      rating: 5,
      text: "I've tried many virtual fitting solutions, but Trylia's accuracy is unmatched. It's like having a personal stylist and fitting room in your pocket!",
      location: "Los Angeles, USA",
      category: "fashion",
      verified: true,
      purchaseCount: 25,
      favoriteFeature: "Size Accuracy"
    },
    {
      id: 4,
      name: "David Kim",
      role: "Business Owner",
      avatar: "👨‍💼",
      rating: 5,
      text: "The convenience is incredible. I can try on multiple outfits in minutes and make confident purchases. Trylia has saved me so much time and money.",
      location: "Chicago, USA",
      category: "business",
      verified: true,
      purchaseCount: 12,
      favoriteFeature: "Time Saving"
    },
    {
      id: 5,
      name: "Lisa Thompson",
      role: "Student",
      avatar: "👩‍🎓",
      rating: 5,
      text: "Perfect for my budget-conscious shopping! I can see exactly how clothes fit before buying, which means no more expensive mistakes.",
      location: "Boston, USA",
      category: "budget",
      verified: true,
      purchaseCount: 6,
      favoriteFeature: "Cost Savings"
    },
    {
      id: 6,
      name: "Alex Martinez",
      role: "Fitness Trainer",
      avatar: "🏋️‍♂️",
      rating: 5,
      text: "Finding athletic wear that fits my build was always challenging. Trylia's body mapping technology is spot-on for fitness apparel!",
      location: "Miami, USA",
      category: "fitness",
      verified: true,
      purchaseCount: 18,
      favoriteFeature: "Body Mapping"
    },
    {
      id: 7,
      name: "Priya Patel",
      role: "Designer",
      avatar: "👩‍🎨",
      rating: 5,
      text: "The color accuracy and fabric visualization are incredible. As a designer, I appreciate the attention to detail in the virtual representation.",
      location: "London, UK",
      category: "design",
      verified: true,
      purchaseCount: 22,
      favoriteFeature: "Color Accuracy"
    },
    {
      id: 8,
      name: "James Wilson",
      role: "Photographer",
      avatar: "📸",
      rating: 5,
      text: "I need to look professional for client meetings. Trylia helps me choose outfits that photograph well and fit perfectly.",
      location: "Toronto, Canada",
      category: "professional",
      verified: true,
      purchaseCount: 14,
      favoriteFeature: "Professional Styling"
    }
  ];

  const videoTestimonials = [
    {
      id: 'v1',
      name: "Jessica Brown",
      role: "Fashion Influencer",
      avatar: "👩‍💄",
      thumbnail: "🎥",
      duration: "2:15",
      views: "125K",
      title: "My Trylia Experience - Game Changer!"
    },
    {
      id: 'v2',
      name: "Ryan Cooper",
      role: "Tech Reviewer",
      avatar: "👨‍💻",
      thumbnail: "📱",
      duration: "3:42",
      views: "89K",
      title: "Trylia AR Technology Review"
    },
    {
      id: 'v3',
      name: "Maria Santos",
      role: "Lifestyle Blogger",
      avatar: "✨",
      thumbnail: "👗",
      duration: "1:58",
      views: "67K",
      title: "Virtual Shopping Haul with Trylia"
    }
  ];

  const categories = [
    { id: 'all', label: 'All Reviews', icon: '⭐' },
    { id: 'fashion', label: 'Fashion', icon: '👗' },
    { id: 'technology', label: 'Technology', icon: '🤖' },
    { id: 'business', label: 'Business', icon: '💼' },
    { id: 'fitness', label: 'Fitness', icon: '🏋️' }
  ];

  const filteredTestimonials = selectedCategory === 'all' 
    ? testimonials 
    : testimonials.filter(t => t.category === selectedCategory);

  useEffect(() => {
    if (!showVideoTestimonials) {
      const interval = setInterval(() => {
        setCurrentTestimonial((prev) => (prev + 1) % filteredTestimonials.length);
      }, 5000);

      return () => clearInterval(interval);
    }
  }, [filteredTestimonials.length, showVideoTestimonials]);

  useEffect(() => {
    setCurrentTestimonial(0);
  }, [selectedCategory]);

  const nextTestimonial = () => {
    setCurrentTestimonial((prev) => (prev + 1) % filteredTestimonials.length);
  };

  const prevTestimonial = () => {
    setCurrentTestimonial((prev) => (prev - 1 + filteredTestimonials.length) % filteredTestimonials.length);
  };

  const goToTestimonial = (index) => {
    setCurrentTestimonial(index);
  };

  return (
    <section className="testimonials" id="testimonials">
      <div className="container">
        <div className="testimonials-header">
          <h2 className="testimonials-title">What Our Customers Say</h2>
          <p className="testimonials-subtitle">
            Join thousands of satisfied customers who've transformed their shopping experience
          </p>
          
          {/* Category Filter */}
          <div className="testimonials-filters">
            {categories.map((category) => (
              <button
                key={category.id}
                className={`filter-btn ${selectedCategory === category.id ? 'active' : ''}`}
                onClick={() => setSelectedCategory(category.id)}
              >
                <span className="filter-icon">{category.icon}</span>
                <span className="filter-label">{category.label}</span>
              </button>
            ))}
          </div>
          
          {/* Toggle Video Testimonials */}
          <div className="testimonials-toggle">
            <button
              className={`toggle-btn ${!showVideoTestimonials ? 'active' : ''}`}
              onClick={() => setShowVideoTestimonials(false)}
            >
              📝 Written Reviews
            </button>
            <button
              className={`toggle-btn ${showVideoTestimonials ? 'active' : ''}`}
              onClick={() => setShowVideoTestimonials(true)}
            >
              🎥 Video Reviews
            </button>
          </div>
        </div>

        <div className="testimonials-carousel">
          <div className="testimonial-container">
            {!showVideoTestimonials ? (
              <div 
                className="testimonials-track"
                style={{ transform: `translateX(-${currentTestimonial * 100}%)` }}
              >
                {filteredTestimonials.map((testimonial, index) => (
                  <div key={testimonial.id} className="testimonial-card">
                    <div className="testimonial-content">
                      <div className="testimonial-header">
                        <div className="testimonial-avatar">
                          <span className="avatar-emoji">{testimonial.avatar}</span>
                          {testimonial.verified && (
                            <div className="verified-badge">✓</div>
                          )}
                        </div>
                        <div className="testimonial-info">
                          <h4 className="testimonial-name">{testimonial.name}</h4>
                          <p className="testimonial-role">{testimonial.role}</p>
                          <p className="testimonial-location">{testimonial.location}</p>
                        </div>
                        <div className="testimonial-rating">
                          {[...Array(testimonial.rating)].map((_, i) => (
                            <span key={i} className="star">⭐</span>
                          ))}
                        </div>
                      </div>
                      <div className="testimonial-text">
                        <div className="quote-icon">"</div>
                        <p>{testimonial.text}</p>
                      </div>
                      <div className="testimonial-footer">
                        <div className="testimonial-stats">
                          <span className="stat">🛍️ {testimonial.purchaseCount} purchases</span>
                          <span className="stat">❤️ {testimonial.favoriteFeature}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="video-testimonials-grid">
                {videoTestimonials.map((video) => (
                  <div key={video.id} className="video-testimonial-card">
                    <div className="video-thumbnail">
                      <div className="thumbnail-content">
                        <span className="thumbnail-icon">{video.thumbnail}</span>
                        <div className="play-overlay">
                          <div className="play-button">
                            <span>▶️</span>
                          </div>
                        </div>
                      </div>
                      <div className="video-duration">{video.duration}</div>
                    </div>
                    <div className="video-info">
                      <div className="video-creator">
                        <span className="creator-avatar">{video.avatar}</span>
                        <div>
                          <h4 className="creator-name">{video.name}</h4>
                          <p className="creator-role">{video.role}</p>
                        </div>
                      </div>
                      <h3 className="video-title">{video.title}</h3>
                      <div className="video-stats">
                        <span className="views">👁️ {video.views} views</span>
                        <span className="rating">⭐ 5.0</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {!showVideoTestimonials && (
            <>
              <div className="testimonials-controls">
                <button 
                  className="testimonial-btn prev-btn"
                  onClick={prevTestimonial}
                  aria-label="Previous testimonial"
                >
                  ←
                </button>
                <button 
                  className="testimonial-btn next-btn"
                  onClick={nextTestimonial}
                  aria-label="Next testimonial"
                >
                  →
                </button>
              </div>

              <div className="testimonials-dots">
                {filteredTestimonials.map((_, index) => (
                  <button
                    key={index}
                    className={`dot ${index === currentTestimonial ? 'active' : ''}`}
                    onClick={() => goToTestimonial(index)}
                    aria-label={`Go to testimonial ${index + 1}`}
                  />
                ))}
              </div>
            </>
          )}
        </div>

        <div className="testimonials-stats">
          <div className="stat-item">
            <div className="stat-number">4.9/5</div>
            <div className="stat-label">Average Rating</div>
          </div>
          <div className="stat-item">
            <div className="stat-number">10K+</div>
            <div className="stat-label">Reviews</div>
          </div>
          <div className="stat-item">
            <div className="stat-number">98%</div>
            <div className="stat-label">Satisfaction Rate</div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Testimonials;