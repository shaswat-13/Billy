import React from 'react';
import './Card.css';

const Card = ({ children, title, emoji, className = '' }) => {
  return (
    <div className={`card paper ${className}`}>
      {(title || emoji) && (
        <div className="card-header">
          {emoji && <span className="card-emoji">{emoji}</span>}
          {title && <h3 className="card-title">{title}</h3>}
        </div>
      )}
      <div className="card-body">
        {children}
      </div>
    </div>
  );
};

export default Card;