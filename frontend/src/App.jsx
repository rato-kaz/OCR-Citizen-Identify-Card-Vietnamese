import React, { useState, useEffect } from 'react';
import ImageUpload from './components/ImageUpload';
import ResultsDisplay from './components/ResultsDisplay';
import Header from './components/Header';
import { ocrAPI } from './services/api';
import './styles/App.css';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [serviceStatus, setServiceStatus] = useState(null);

  // Check service health on component mount
  useEffect(() => {
    checkServiceHealth();
  }, []);

  const checkServiceHealth = async () => {
    try {
      const health = await ocrAPI.healthCheck();
      setServiceStatus(health);
    } catch (err) {
      console.error('Service health check failed:', err);
      setServiceStatus({ status: 'unhealthy' });
    }
  };

  const handleImageUpload = async (file) => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await ocrAPI.detectText(file);
      setResults(response);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to process image');
      console.error('OCR processing failed:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResults(null);
    setError(null);
  };

  return (
    <div className="app">
      <Header serviceStatus={serviceStatus} />
      
      <main className="main-content">
        <div className="container">
          <div className="upload-section">
            <ImageUpload 
              onUpload={handleImageUpload}
              loading={loading}
              disabled={serviceStatus?.status !== 'healthy'}
            />
          </div>

          {error && (
            <div className="error-message">
              <h3>Error</h3>
              <p>{error}</p>
              <button onClick={handleReset} className="retry-btn">
                Try Again
              </button>
            </div>
          )}

          {results && (
            <ResultsDisplay 
              results={results}
              onReset={handleReset}
            />
          )}
        </div>
      </main>
    </div>
  );
}

export default App;

