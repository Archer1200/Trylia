import React from 'react';
import ProductCard from '../components/ProductCard';
import '../styles/Catalog.css';

const Catalog = () => {
  // Male products (7 shirts)
  const maleProducts = Array.from({ length: 7 }, (_, i) => ({
    id: i + 1,
    name: `Men's Shirt ${i + 1}`,
    image: `/images/male/shirt${i + 1}.png`,
    category: 'Male'
  }));

  // Female products (5 shirts)
  const femaleProducts = Array.from({ length: 5 }, (_, i) => ({
    id: i + 101,
    name: `Women's Shirt ${i + 1}`,
    image: `/images/female/shirt${i + 1}.png`,
    category: 'Female'
  }));

  // Combine both categories
  const products = [...maleProducts, ...femaleProducts];

  return (
    <div className="catalog">
      <div className="container">
        <div className="catalog-header">
          <h1>Our Virtual Try-On Collection</h1>
          <p>Try out our stylish shirts virtually — available for everyone!</p>
        </div>

        <div className="products-grid">
          {products.map(product => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Catalog;
