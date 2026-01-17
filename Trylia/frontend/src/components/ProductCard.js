import React, { useState, useEffect } from 'react';
import '../styles/ProductCard.css';

const ProductCard = ({ product }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isRunning, setIsRunning] = useState(false);

  // Check service status periodically
  useEffect(() => {
    const checkStatus = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/status');
        const data = await response.json();
        setIsRunning(data.isRunning);
      } catch (err) {
        setIsRunning(false);
      }
    };

    checkStatus();
    const interval = setInterval(checkStatus, 2000); // Check every 2 seconds
    return () => clearInterval(interval);
  }, []);

  const handleTryOn = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:5000/api/try-on', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          shirtId: product.id
        })
      });
      
      const data = await response.json();
      
      if (data.success) {
        setIsRunning(true);
        alert(`Virtual try-on started for "${product.name}"! The camera window will open shortly. Press 'q' in the camera window to stop.`);
      } else {
        throw new Error(data.message || 'Failed to start virtual try-on');
      }
    } catch (err) {
      console.error('Error starting virtual try-on:', err);
      setError(err.message);
      alert(`Error: ${err.message}. Make sure the backend server is running on http://localhost:5000`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleStop = async () => {
    setIsLoading(true);
    
    try {
      const response = await fetch('http://localhost:5000/api/stop', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      
      const data = await response.json();
      
      if (data.success) {
        setIsRunning(false);
        alert('Virtual try-on stopped successfully!');
      } else {
        throw new Error(data.message || 'Failed to stop virtual try-on');
      }
    } catch (err) {
      console.error('Error stopping virtual try-on:', err);
      alert(`Error: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="product-card">
      <div className="product-image">
        <img src={product.image} alt={product.name} />
        <div className="product-overlay">
          <button className="quick-view-btn">Quick View</button>
        </div>
      </div>
      <div className="product-info">
        <h3 className="product-name">{product.name}</h3>
        <p className="product-category">{product.category}</p>
        <div className="product-footer">
          {/* <span className="product-price">${product.price}</span> */}
          <div className="button-group">
            <button 
              className={`try-on-btn ${isRunning ? 'running' : ''}`}
              onClick={handleTryOn}
              disabled={isLoading || isRunning}
            >
              {isLoading ? 'Starting...' : isRunning ? 'Running' : 'Try On'}
            </button>
            {isRunning && (
              <button 
                className="stop-btn"
                onClick={handleStop}
                disabled={isLoading}
              >
                {isLoading ? 'Stopping...' : 'Stop'}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;