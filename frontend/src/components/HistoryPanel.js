import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './HistoryPanel.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const HistoryPanel = ({ isOpen, onClose }) => {
  const [history, setHistory] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isOpen) {
      loadHistory();
    }
  }, [isOpen]);

  const loadHistory = async () => {
    setLoading(true);
    setError(null);

    try {
      const sessionId = localStorage.getItem('heart_prediction_session');
      if (!sessionId) {
        setError('No session found. Make a prediction first.');
        return;
      }

      const response = await axios.get(`${API_BASE_URL}/history/${sessionId}`);
      setHistory(response.data);
    } catch (error) {
      console.error('Error loading history:', error);
      if (error.response?.status === 404) {
        setError('No prediction history found.');
      } else {
        setError('Failed to load history. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const exportData = async () => {
    try {
      const sessionId = localStorage.getItem('heart_prediction_session');
      const response = await axios.get(`${API_BASE_URL}/export/${sessionId}`);
      
      // Create and download file
      const dataStr = JSON.stringify(response.data, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `heart_prediction_history_${sessionId}.json`;
      link.click();
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Export error:', error);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="history-overlay">
      <div className="history-panel">
        <div className="history-header">
          <h2>
            <i className="fas fa-history"></i>
            Prediction History
          </h2>
          <button onClick={onClose} className="close-button">
            <i className="fas fa-times"></i>
          </button>
        </div>

        <div className="history-content">
          {loading && (
            <div className="loading-state">
              <div className="spinner"></div>
              <p>Loading history...</p>
            </div>
          )}

          {error && (
            <div className="error-state">
              <i className="fas fa-exclamation-triangle"></i>
              <p>{error}</p>
            </div>
          )}

          {history && (
            <>
              <div className="history-summary">
                <div className="summary-card">
                  <h3>Session Summary</h3>
                  <p><strong>Total Predictions:</strong> {history.predictions.length}</p>
                  <p><strong>Session ID:</strong> {history.user.session_id}</p>
                  <p><strong>Started:</strong> {new Date(history.user.created_at).toLocaleString()}</p>
                  <button onClick={exportData} className="export-button">
                    <i className="fas fa-download"></i>
                    Export Data
                  </button>
                </div>
              </div>

              <div className="predictions-list">
                <h3>Previous Predictions</h3>
                {history.predictions.length === 0 ? (
                  <p className="no-predictions">No predictions found.</p>
                ) : (
                  history.predictions.map((prediction) => (
                    <div key={prediction.id} className="prediction-item">
                      <div className="prediction-header">
                        <span className="prediction-date">
                          {new Date(prediction.created_at).toLocaleString()}
                        </span>
                        <span className={`risk-badge ${prediction.prediction_results.risk_level.toLowerCase()}`}>
                          {prediction.prediction_results.risk_level} Risk ({prediction.prediction_results.risk_percentage}%)
                        </span>
                      </div>
                      <div className="prediction-details">
                        <div className="result">
                          <strong>Result:</strong> {prediction.prediction_results.prediction === 1 ? 'Heart Disease Detected' : 'No Heart Disease Detected'}
                        </div>
                        <div className="confidence">
                          <strong>Confidence:</strong> {prediction.prediction_results.confidence}%
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default HistoryPanel;