import React from 'react';
import './homepage.css';

import robot from './MBot_spotlight_square.jpg';

const HomePage = () => {
  return (
    <div className="home-page">
      <div className="hero-section">
        <h1>Welcome to the Mbot Web Application</h1>
        <p>A revolutionary platform for all your bot-building needs</p>
      </div>
      <div className="image-section">
        <img src={robot} alt="Image 1" />
      </div>
    </div>
  );
};

export default HomePage;