import React from 'react';
import { Link } from 'react-router-dom';
import Logo from '../components/Logo';
import Button from '../components/Button';
import Card from '../components/Card';
import './LandingPage.css';

const LandingPage = () => {
  return (
    <div className="landing-page">
      <div className="hero">
        <Logo size="large" />
        <h1 className="hero-title">
          Your Personal Expense Tracker
          <br />
          <span className="highlight">With Bumblebee Energy! 🐝</span>
        </h1>
        <p className="hero-subtitle">
          Track expenses. Manage income. Stay on top of your finances.
        </p>
        <div className="hero-buttons">
          <Link to="/signup">
            <Button variant="primary" size="large">
              Get Started Free
            </Button>
          </Link>
          <Link to="/login">
            <Button variant="secondary" size="large">
              Login
            </Button>
          </Link>
        </div>
      </div>

      <div className="features">
        <Card emoji="💰" title="Track Income">
          <p>Record all your income sources. Salary, freelance, gifts - track it all in one place.</p>
        </Card>

        <Card emoji="📊" title="Manage Expenses">
          <p>Log every expense with ease. See exactly where your money goes each month.</p>
        </Card>

        <Card emoji="📈" title="Financial Summary">
          <p>Get instant insights. See your balance, totals, and financial health at a glance.</p>
        </Card>
      </div>
    </div>
  );
};

export default LandingPage;