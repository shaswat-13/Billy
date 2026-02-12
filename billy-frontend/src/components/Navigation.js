import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Logo from './Logo';
import Button from './Button';
import { authAPI } from '../services/api';
import './Navigation.css';

const Navigation = ({ isAuthenticated, setIsAuthenticated }) => {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await authAPI.logout();
      setIsAuthenticated(false);
      navigate('/');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <nav className="navigation paper">
      <div className="nav-container">
        <Link to="/" className="nav-logo">
          <Logo size="small" />
        </Link>

        <div className="nav-links">
          {isAuthenticated ? (
            <>
              <Link to="/dashboard" className="nav-link">Dashboard</Link>
              <Button variant="secondary" size="small" onClick={handleLogout}>
                Logout
              </Button>
            </>
          ) : (
            <>
              <Link to="/login" className="nav-link">Login</Link>
              <Link to="/signup">
                <Button variant="primary" size="small">Sign Up</Button>
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navigation;