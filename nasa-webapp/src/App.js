import React, { useState, useEffect } from 'react';
import { Button, Card, CardContent, CardMedia, Typography, CircularProgress } from '@mui/material';
import axios from 'axios';
import './index.css';

// StarField Component
const StarField = () => {
  const starCount = 200;
  const starsArray = new Array(starCount).fill(0);

  return (
    <div className="star-field">
      {starsArray.map((_, index) => {
        const size = Math.random() * 3 + 1;
        const xPos = Math.random() * 100;
        const yPos = Math.random() * 100;
        const delay = Math.random() * 2;

        return (
          <div
            key={index}
            className="star"
            style={{
              width: `${size}px`,
              height: `${size}px`,
              top: `${yPos}vh`,
              left: `${xPos}vw`,
              animationDelay: `${delay}s`,
            }}
          ></div>
        );
      })}
    </div>
  );
};


// App with Photo Card and refresh button
const App = () => {
  const [photo, setPhoto] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchPhoto = async () => {
    setLoading(true);
    try {
      const response = await axios.get("http://localhost:8000/v1/photo");
      setPhoto(response.data);
    } catch (error) {
      console.error("Error fetching photo", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPhoto();
  }, []);

  return (
    <div className="app-container">
      <StarField />
      <div className="content-container">
        {loading ? (
          <CircularProgress />
        ) : photo ? (
          <Card className="photo-card">
            <CardMedia component="img" height="400" image={photo.url} alt={photo.title} />
            <CardContent className="card-content">
              <Typography gutterBottom variant="h5" component="h2">{photo.title}</Typography>
              <Typography variant="body1" aria-label="description">
                {photo.explanation}
              </Typography>
            </CardContent>
          </Card>
        ) : (
          <p className="no-photo-text">No photo available</p>
        )}
        <div className="button-container">
          <Button variant="contained" color="primary" onClick={fetchPhoto}>
            New Photo
          </Button>
        </div>
      </div>
    </div>
  );
};

export default App;
