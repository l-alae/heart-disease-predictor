import React, { useState } from 'react';
import './PredictionForm.css';

const PredictionForm = ({ features, onSubmit, loading, formData, setFormData }) => {
  const [errors, setErrors] = useState({});

  const handleInputChange = (name, value) => {
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    features.feature_order.forEach(feature => {
      const value = formData[feature];
      const featureInfo = features.features[feature];
      
      if (value === '' || value === null || value === undefined) {
        newErrors[feature] = `${featureInfo.name} is required`;
        return;
      }
      
      const numValue = parseFloat(value);
      if (isNaN(numValue)) {
        newErrors[feature] = `${featureInfo.name} must be a valid number`;
        return;
      }
      
      // Range validation for numeric fields
      if (featureInfo.min !== undefined && numValue < featureInfo.min) {
        newErrors[feature] = `${featureInfo.name} must be at least ${featureInfo.min}`;
      }
      if (featureInfo.max !== undefined && numValue > featureInfo.max) {
        newErrors[feature] = `${featureInfo.name} must be at most ${featureInfo.max}`;
      }
    });
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateForm()) {
      onSubmit(formData);
    }
  };

  const renderField = (feature) => {
    const featureInfo = features.features[feature];
    const value = formData[feature] || '';
    const error = errors[feature];

    if (featureInfo.options) {
      // Render select dropdown for categorical variables
      return (
        <div key={feature} className="form-group">
          <label htmlFor={feature} className="form-label">
            {featureInfo.name}
            <span className="required">*</span>
          </label>
          <select
            id={feature}
            value={value}
            onChange={(e) => handleInputChange(feature, e.target.value)}
            className={`form-select ${error ? 'error' : ''}`}
            disabled={loading}
          >
            <option value="">Select {featureInfo.name}</option>
            {Object.entries(featureInfo.options).map(([key, label]) => (
              <option key={key} value={key}>
                {label}
              </option>
            ))}
          </select>
          {error && <span className="error-message">{error}</span>}
        </div>
      );
    } else {
      // Render numeric input
      return (
        <div key={feature} className="form-group">
          <label htmlFor={feature} className="form-label">
            {featureInfo.name}
            {featureInfo.unit && <span className="unit">({featureInfo.unit})</span>}
            <span className="required">*</span>
          </label>
          <input
            type="number"
            id={feature}
            value={value}
            onChange={(e) => handleInputChange(feature, e.target.value)}
            className={`form-input ${error ? 'error' : ''}`}
            placeholder={`Enter ${featureInfo.name.toLowerCase()}`}
            min={featureInfo.min}
            max={featureInfo.max}
            step={feature === 'oldpeak' ? '0.1' : '1'}
            disabled={loading}
          />
          {featureInfo.min !== undefined && featureInfo.max !== undefined && (
            <span className="range-hint">
              Range: {featureInfo.min} - {featureInfo.max} {featureInfo.unit || ''}
            </span>
          )}
          {error && <span className="error-message">{error}</span>}
        </div>
      );
    }
  };

  return (
    <form onSubmit={handleSubmit} className="prediction-form">
      <div className="form-grid">
        {features.feature_order.map(renderField)}
      </div>
      
      <div className="form-actions">
        <button
          type="submit"
          className="submit-button"
          disabled={loading}
        >
          {loading ? (
            <>
              <div className="button-spinner"></div>
              Analyzing...
            </>
          ) : (
            <>
              <i className="fas fa-chart-line"></i>
              Predict Risk
            </>
          )}
        </button>
      </div>
    </form>
  );
};

export default PredictionForm;