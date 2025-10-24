import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import PredictionForm from './components/PredictionForm';
import ResultDisplay from './components/ResultDisplay';
import HistoryPanel from './components/HistoryPanel';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [features, setFeatures] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [formData, setFormData] = useState({});
  const [showHistory, setShowHistory] = useState(false);

  useEffect(() => {
    // Fetch feature information from backend
    const fetchFeatures = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/features`);
        setFeatures(response.data);
        
        // Initialize form data with default values
        const initialData = {};
        response.data.feature_order.forEach(feature => {
          initialData[feature] = '';
        });
        setFormData(initialData);
      } catch (error) {
        console.error('Error fetching features:', error);
        toast.error('Failed to load application data. Please refresh the page.');
      }
    };

    fetchFeatures();
  }, []);

  const handleSubmit = async (data) => {
    setLoading(true);
    setResult(null);

    try {
      // Get or create session ID
      let sessionId = localStorage.getItem('heart_prediction_session');
      if (!sessionId) {
        sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('heart_prediction_session', sessionId);
      }

      // Add session ID to headers
      const response = await axios.post(`${API_BASE_URL}/predict`, data, {
        headers: {
          'X-Session-ID': sessionId
        }
      });
      
      setResult(response.data);
      
      // Show success message with prediction ID if available
      const message = response.data.prediction_id 
        ? `Prediction completed successfully! (ID: ${response.data.prediction_id})`
        : 'Prediction completed successfully!';
      toast.success(message);
      
    } catch (error) {
      console.error('Prediction error:', error);
      const errorMessage = error.response?.data?.error || 'Failed to get prediction. Please try again.';
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    if (features) {
      const initialData = {};
      features.feature_order.forEach(feature => {
        initialData[feature] = '';
      });
      setFormData(initialData);
    }
  };

  if (!features) {
    return (
      <div className="app">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading application...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <div className="header-icon">
            <i className="fas fa-heartbeat"></i>
          </div>
          <div className="header-text">
            <h1>Heart Disease Prediction</h1>
            <p>AI-powered cardiovascular risk assessment</p>
          </div>
          <div className="header-actions">
            <button 
              onClick={() => setShowHistory(true)} 
              className="history-button"
              title="View Prediction History"
            >
              <i className="fas fa-history"></i>
              History
            </button>
          </div>
        </div>
      </header>

      <main className="app-main">
        <div className="container">
          <div className="app-grid">
            <div className="form-section">
              <div className="section-header">
                <h2>
                  <i className="fas fa-user-md"></i>
                  Patient Information
                </h2>
                <p>Please fill in all the medical parameters below</p>
              </div>
              <PredictionForm
                features={features}
                onSubmit={handleSubmit}
                loading={loading}
                formData={formData}
                setFormData={setFormData}
              />
            </div>

            <div className="result-section">
              <div className="section-header">
                <h2>
                  <i className="fas fa-chart-line"></i>
                  Risk Assessment
                </h2>
                <p>Your cardiovascular risk analysis will appear here</p>
              </div>
              {result ? (
                <ResultDisplay result={result} onReset={handleReset} />
              ) : (
                <div className="no-result">
                  <div className="no-result-icon">
                    <i className="fas fa-clipboard-list"></i>
                  </div>
                  <p>Complete the form to get your risk assessment</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>

      <footer className="app-footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-disclaimer">
              <i className="fas fa-exclamation-triangle"></i>
              <p>
                <strong>Medical Disclaimer:</strong> This tool is for educational purposes only. 
                Always consult with healthcare professionals for medical advice.
              </p>
            </div>
            <div className="footer-info">
              <p>&copy; 2024 Heart Disease Prediction App</p>
            </div>
          </div>
        </div>
      </footer>

      <HistoryPanel 
        isOpen={showHistory} 
        onClose={() => setShowHistory(false)} 
      />

      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="light"
      />
    </div>
  );
}

export default App;