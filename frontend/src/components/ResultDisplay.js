import React from 'react';
import './ResultDisplay.css';

const ResultDisplay = ({ result, onReset }) => {
  const {
    prediction,
    risk_percentage,
    risk_level,
    risk_color,
    interpretation
  } = result;

  const getRiskIcon = () => {
    switch (risk_level) {
      case 'Low':
        return 'fas fa-shield-alt';
      case 'Moderate':
        return 'fas fa-exclamation-triangle';
      case 'High':
        return 'fas fa-exclamation-circle';
      default:
        return 'fas fa-question-circle';
    }
  };

  const getCircumference = () => 2 * Math.PI * 45;
  const getStrokeDasharray = () => {
    const circumference = getCircumference();
    const progress = (risk_percentage / 100) * circumference;
    return `${progress} ${circumference}`;
  };

  return (
    <div className="result-display">
      <div className="result-header">
        <div className="result-icon" style={{ color: risk_color }}>
          <i className={getRiskIcon()}></i>
        </div>
        <h3>Risk Assessment Complete</h3>
      </div>

      <div className="risk-meter">
        <div className="risk-circle">
          <svg className="risk-svg" viewBox="0 0 100 100">
            <circle
              cx="50"
              cy="50"
              r="45"
              fill="none"
              stroke="#e9ecef"
              strokeWidth="8"
            />
            <circle
              cx="50"
              cy="50"
              r="45"
              fill="none"
              stroke={risk_color}
              strokeWidth="8"
              strokeLinecap="round"
              strokeDasharray={getStrokeDasharray()}
              transform="rotate(-90 50 50)"
              className="risk-progress"
            />
          </svg>
          <div className="risk-percentage">
            <span className="percentage-number">{risk_percentage}%</span>
            <span className="percentage-label">Risk</span>
          </div>
        </div>
      </div>

      <div className="risk-level-badge" style={{ backgroundColor: risk_color }}>
        <i className={getRiskIcon()}></i>
        {risk_level} Risk
      </div>

      <div className="result-details">
        <div className="detail-card">
          <div className="detail-header">
            <i className="fas fa-diagnosis"></i>
            <h4>Diagnosis</h4>
          </div>
          <p className="detail-value">{interpretation.result}</p>
        </div>

        <div className="detail-card">
          <div className="detail-header">
            <i className="fas fa-chart-bar"></i>
            <h4>Confidence</h4>
          </div>
          <p className="detail-value">{interpretation.confidence}</p>
        </div>

        <div className="detail-card full-width">
          <div className="detail-header">
            <i className="fas fa-lightbulb"></i>
            <h4>Recommendation</h4>
          </div>
          <p className="detail-recommendation">{interpretation.recommendation}</p>
        </div>
      </div>

      <div className="result-actions">
        <button onClick={onReset} className="reset-button">
          <i className="fas fa-redo"></i>
          New Assessment
        </button>
        <button 
          onClick={() => window.print()} 
          className="print-button"
        >
          <i className="fas fa-print"></i>
          Print Results
        </button>
      </div>

      <div className="result-disclaimer">
        <i className="fas fa-info-circle"></i>
        <p>
          This prediction is based on machine learning analysis and should not replace 
          professional medical consultation. Please consult with a healthcare provider 
          for proper medical evaluation.
        </p>
      </div>
    </div>
  );
};

export default ResultDisplay;