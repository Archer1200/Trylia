import React, { useState, useEffect } from 'react';
import '../styles/AboutPage.css';

const About = () => {
  const [activeTab, setActiveTab] = useState('story');
  const [isVisible, setIsVisible] = useState({});

  // Intersection Observer for animations
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsVisible(prev => ({
              ...prev,
              [entry.target.id]: true
            }));
          }
        });
      },
      { threshold: 0.1 }
    );

    const elements = document.querySelectorAll('[data-animate]');
    elements.forEach((el) => observer.observe(el));

    return () => observer.disconnect();
  }, []);

  const stats = [
    { number: '50K+', label: 'Happy Customers', icon: '👥' },
    { number: '1M+', label: 'Virtual Try-Ons', icon: '👗' },
    { number: '500+', label: 'Brand Partners', icon: '🤝' },
    { number: '99%', label: 'Accuracy Rate', icon: '🎯' },
    { number: '24/7', label: 'Support', icon: '💬' },
    // { number: '150+', label: 'Countries', icon: '🌍' }
  ];

  const timeline = [
    {
      year: '2024',
      title: 'Trylia Launch',
      description: 'Revolutionary virtual try-on technology debuts with AI-powered body mapping.',
      icon: '🚀'
    },
    {
      year: '2024',
      title: 'First Million Try-Ons',
      description: 'Reached 1 million virtual try-on sessions within first 6 months.',
      icon: '🎉'
    },
    {
      year: '2024',
      title: 'Global Expansion',
      description: 'Expanded to 150+ countries with localized shopping experiences.',
      icon: '🌐'
    },
    {
      year: '2024',
      title: 'AI Enhancement',
      description: 'Introduced advanced AI algorithms for 99% size accuracy.',
      icon: '🤖'
    }
  ];

  const team = [
    {
      name: 'Sarah Chen',
      role: 'CEO & Founder',
      avatar: '👩‍💼',
      bio: 'Former fashion tech executive with 15+ years experience in retail innovation.',
      expertise: ['Leadership', 'Strategy', 'Fashion Tech']
    },
    {
      name: 'Marcus Rodriguez',
      role: 'CTO',
      avatar: '👨‍💻',
      bio: 'AI and computer vision expert, previously at leading tech companies.',
      expertise: ['AI/ML', 'Computer Vision', 'AR Technology']
    },
    {
      name: 'Emily Johnson',
      role: 'Head of Design',
      avatar: '👩‍🎨',
      bio: 'Award-winning UX designer focused on creating intuitive shopping experiences.',
      expertise: ['UX Design', 'User Research', 'Product Design']
    },
    {
      name: 'David Kim',
      role: 'VP of Engineering',
      avatar: '👨‍🔧',
      bio: 'Full-stack engineer with expertise in scalable web applications.',
      expertise: ['Full-Stack', 'Cloud Architecture', 'DevOps']
    }
  ];

  const values = [
    {
      title: 'Innovation',
      description: 'Pushing the boundaries of fashion technology to create better shopping experiences.',
      icon: '💡'
    },
    {
      title: 'Accessibility',
      description: 'Making fashion accessible to everyone, regardless of location or physical limitations.',
      icon: '🌟'
    },
    {
      title: 'Sustainability',
      description: 'Reducing returns and waste through accurate virtual try-on technology.',
      icon: '🌱'
    },
    {
      title: 'Quality',
      description: 'Delivering premium experiences with attention to every detail.',
      icon: '✨'
    }
  ];

  return (
    <div className="about-page">
      {/* Hero Section */}
      <section className="about-hero">
        <div className="container">
          <div className="hero-content" data-animate id="hero">
            <h1 className={`hero-title ${isVisible.hero ? 'animate' : ''}`}>
              About Trylia
            </h1>
            <p className={`hero-subtitle ${isVisible.hero ? 'animate' : ''}`}>
              Revolutionizing Fashion with Virtual Reality
            </p>
            <p className={`hero-description ${isVisible.hero ? 'animate' : ''}`}>
              We're on a mission to transform how people shop for clothes by combining 
              cutting-edge AI technology with the convenience of online shopping.
            </p>
          </div>
        </div>
      </section>

      {/* Navigation Tabs */}
      <section className="about-nav">
        <div className="container">
          <div className="nav-tabs">
            <button 
              className={`tab-btn ${activeTab === 'story' ? 'active' : ''}`}
              onClick={() => setActiveTab('story')}
            >
              Our Story
            </button>
            {/* <button 
              className={`tab-btn ${activeTab === 'team' ? 'active' : ''}`}
              onClick={() => setActiveTab('team')}
            >
              Our Team
            </button>
            <button 
              className={`tab-btn ${activeTab === 'values' ? 'active' : ''}`}
              onClick={() => setActiveTab('values')}
            >
              Our Values
            </button>
            <button 
              className={`tab-btn ${activeTab === 'timeline' ? 'active' : ''}`}
              onClick={() => setActiveTab('timeline')}
            >
              Timeline
            </button> */}
          </div>
        </div>
      </section>

      {/* Tab Content */}
      <section className="tab-content">
        <div className="container">
          {activeTab === 'story' && (
            <div className="story-content" data-animate id="story">
              <div className={`content-grid ${isVisible.story ? 'animate' : ''}`}>
                <div className="story-text">
                  <h2>The Trylia Story</h2>
                  <p>
                    Born from the frustration of online shopping uncertainties, Trylia emerged 
                    as a solution to the age-old question: "Will this look good on me?" Our 
                    founders, having experienced countless returns and sizing disappointments, 
                    envisioned a world where you could try before you buy, virtually.
                  </p>
                  <p>
                    What started as a simple idea has evolved into a revolutionary platform 
                    that uses advanced AI and augmented reality to create the most accurate 
                    virtual fitting room experience available today.
                  </p>
                  <div className="story-highlights">
                    <div className="highlight">
                      <span className="highlight-icon">🎯</span>
                      <div>
                        <h4>Our Mission</h4>
                        <p>To eliminate the guesswork from online fashion shopping</p>
                      </div>
                    </div>
                    <div className="highlight">
                      <span className="highlight-icon">🔮</span>
                      <div>
                        <h4>Our Vision</h4>
                        <p>A world where every online purchase fits perfectly</p>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="story-visual">
                  <div className="tech-showcase">
                    <h3>Our Technology</h3>
                    <div className="tech-features">
                      <div className="tech-item">
                        <span className="tech-icon">🤖</span>
                        <div>
                          <h4>AI Body Mapping</h4>
                          <p>Advanced algorithms analyze your body measurements with precision</p>
                        </div>
                      </div>
                      <div className="tech-item">
                        <span className="tech-icon">📱</span>
                        <div>
                          <h4>AR Visualization</h4>
                          <p>Real-time augmented reality for lifelike clothing visualization</p>
                        </div>
                      </div>
                      <div className="tech-item">
                        <span className="tech-icon">🎯</span>
                        <div>
                          <h4>Perfect Fit Algorithm</h4>
                          <p>Machine learning ensures 99% accuracy in size recommendations</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'team' && (
            <div className="team-content" data-animate id="team">
              <div className={`team-header ${isVisible.team ? 'animate' : ''}`}>
                <h2>Meet Our Team</h2>
                <p>The brilliant minds behind Trylia's revolutionary technology</p>
              </div>
              <div className={`team-grid ${isVisible.team ? 'animate' : ''}`}>
                {team.map((member, index) => (
                  <div key={index} className="team-card">
                    <div className="member-avatar">
                      <span className="avatar-emoji">{member.avatar}</span>
                    </div>
                    <div className="member-info">
                      <h3>{member.name}</h3>
                      <p className="member-role">{member.role}</p>
                      <p className="member-bio">{member.bio}</p>
                      <div className="member-expertise">
                        {member.expertise.map((skill, skillIndex) => (
                          <span key={skillIndex} className="skill-tag">{skill}</span>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'values' && (
            <div className="values-content" data-animate id="values">
              <div className={`values-header ${isVisible.values ? 'animate' : ''}`}>
                <h2>Our Core Values</h2>
                <p>The principles that guide everything we do</p>
              </div>
              <div className={`values-grid ${isVisible.values ? 'animate' : ''}`}>
                {values.map((value, index) => (
                  <div key={index} className="value-card">
                    <div className="value-icon">{value.icon}</div>
                    <h3>{value.title}</h3>
                    <p>{value.description}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'timeline' && (
            <div className="timeline-content" data-animate id="timeline">
              <div className={`timeline-header ${isVisible.timeline ? 'animate' : ''}`}>
                <h2>Our Journey</h2>
                <p>Key milestones in Trylia's evolution</p>
              </div>
              <div className={`timeline ${isVisible.timeline ? 'animate' : ''}`}>
                {timeline.map((event, index) => (
                  <div key={index} className="timeline-item">
                    <div className="timeline-marker">
                      <span className="timeline-icon">{event.icon}</span>
                    </div>
                    <div className="timeline-content-item">
                      <div className="timeline-year">{event.year}</div>
                      <h3>{event.title}</h3>
                      <p>{event.description}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </section>

      {/* Stats Section */}
      <section className="stats-section" data-animate id="stats">
        <div className="container">
          <div className={`stats-header ${isVisible.stats ? 'animate' : ''}`}>
            <h2>Trylia by the Numbers</h2>
            <p>Our impact on the fashion industry</p>
          </div>
          <div className={`stats-grid ${isVisible.stats ? 'animate' : ''}`}>
            {stats.map((stat, index) => (
              <div key={index} className="stat-card">
                <div className="stat-icon">{stat.icon}</div>
                <div className="stat-number">{stat.number}</div>
                <div className="stat-label">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section" data-animate id="cta">
        <div className="container">
          <div className={`cta-content ${isVisible.cta ? 'animate' : ''}`}>
            <h2>Ready to Experience the Future of Fashion?</h2>
            <p>Join millions of satisfied customers who've revolutionized their shopping experience</p>
            <div className="cta-buttons">
              <a href="/catalog" className="cta-btn primary">Try_On</a>
              {/* <a href="#contact" className="cta-btn secondary">Contact Us</a> */}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default About;