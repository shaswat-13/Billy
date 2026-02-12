import React from 'react';
import './Logo.css';

const Logo = ({ size = 'large' }) => {
  return (
    <div className={`logo logo-${size}`}>
      <span className="logo-cat">🐱</span>
      <span className="logo-text">
        <span className="logo-bil">bil</span>
        <span className="logo-dot">.</span>
        <span className="logo-ly">ly</span>
      </span>
    </div>
  );
};

export default Logo;