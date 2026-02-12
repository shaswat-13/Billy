import React from 'react';
import Logo from './components/Logo';
import Button from './components/Button';
import Card from './components/Card';
import './App.css';

function App() {
  return (
    <div className="app">
      <div className="container">
        <header className="app-header">
          <Logo size="large" />
          <p className="tagline">Your personal expense tracker with bumblebee energy! 🐝</p>
        </header>

        <Card title="Design System Preview" emoji="🎨">
          <h2>Buttons</h2>
          <div style={{ display: 'flex', gap: '16px', marginBottom: '24px' }}>
            <Button variant="primary">Primary Button</Button>
            <Button variant="secondary">Secondary Button</Button>
            <Button variant="danger">Delete</Button>
          </div>

          <h2>Colors</h2>
          <div className="color-grid">
            <div className="color-box" style={{ background: '#FFD60A' }}>Yellow</div>
            <div className="color-box" style={{ background: '#1A1A1A', color: '#fff' }}>Black</div>
            <div className="color-box" style={{ background: '#FFFFFF', border: '2px solid #000' }}>White</div>
          </div>

          <h2>Typography</h2>
          <h1>Heading 1 - Bold & Big</h1>
          <h2>Heading 2 - Still Bold</h2>
          <h3>Heading 3 - You get it</h3>
          <p>Body text - Inter Regular, clean and readable.</p>
          <p className="bold">Bold text for emphasis!</p>
        </Card>

        <Card title="Paper Effect" emoji="📄">
          <p>This card has a paper/bill aesthetic with:</p>
          <ul>
            <li>Black border</li>
            <li>Shadow effect</li>
            <li>Subtle line texture</li>
            <li>Hover animation</li>
          </ul>
        </Card>
      </div>
    </div>
  );
}

export default App;