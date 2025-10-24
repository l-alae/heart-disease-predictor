# Heart Disease Prediction App 🫀

ReactJS, Flask, Scikit-learn, Docker 
A comprehensive full-stack web application that uses machine learning to predict cardiovascular disease risk based on patient medical data. Built with Flask (Python) backend and React frontend, containerized with Docker.

## 🌟 Features

- **AI-Powered Predictions**: Uses a trained Logistic Regression model to assess heart disease risk
- **Interactive Web Interface**: Beautiful, responsive React frontend with real-time form validation
- **Risk Visualization**: Intuitive circular progress indicators and color-coded risk levels
- **Comprehensive Results**: Detailed risk assessment with medical recommendations
- **Professional Design**: Modern UI/UX with smooth animations and responsive design
- **Containerized Deployment**: Easy deployment with Docker and docker-compose
- **Health Monitoring**: Built-in health checks for both frontend and backend services
- **PostgreSQL Integration**: Persistent data storage for user sessions and predictions
- **Prediction History**: Track and review previous predictions with export functionality
- **Session Management**: User sessions with persistent storage across browser sessions
- **Data Analytics**: Application statistics and usage analytics

## 🏗️ Architecture

```
┌─────────────────┐    HTTP/JSON    ┌─────────────────┐    SQL/ORM    ┌─────────────────┐
│                 │    Requests     │                 │   Queries     │                 │
│  React Frontend │◄───────────────►│  Flask Backend  │◄─────────────►│  PostgreSQL DB  │
│   (Port 3000)   │                 │   (Port 5000)   │               │   (Port 5432)   │
│                 │                 │                 │               │                 │
└─────────────────┘                 └─────────────────┘               └─────────────────┘
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │  ML Model       │
                                    │  - model.pkl    │
                                    │  - scaler.pkl   │
                                    └─────────────────┘
```

## 📋 Medical Parameters

The application analyzes the following medical parameters:

| Parameter | Description | Type | Range/Options |
|-----------|-------------|------|---------------|
| **Age** | Patient's age in years | Numeric | 1-120 |
| **Sex** | Patient's gender | Categorical | Male/Female |
| **CP** | Chest pain type | Categorical | Typical Angina, Atypical Angina, Non-Anginal Pain, Asymptomatic |
| **Trestbps** | Resting blood pressure (mm Hg) | Numeric | 80-200 |
| **Chol** | Serum cholesterol (mg/dl) | Numeric | 100-600 |
| **FBS** | Fasting blood sugar > 120 mg/dl | Boolean | True/False |
| **Restecg** | Resting ECG results | Categorical | Normal, ST-T Wave Abnormality, Left Ventricular Hypertrophy |
| **Thalach** | Maximum heart rate achieved | Numeric | 60-220 |
| **Exang** | Exercise induced angina | Boolean | Yes/No |
| **Oldpeak** | ST depression induced by exercise | Numeric | 0-10 |
| **Slope** | Slope of peak exercise ST segment | Categorical | Upsloping, Flat, Downsloping |
| **CA** | Number of major vessels colored by fluoroscopy | Categorical | 0, 1, 2, 3 |
| **Thal** | Thalassemia | Categorical | Normal, Fixed Defect, Reversible Defect |

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed on your system
- Git for cloning the repository

### Option 1: Using Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd disease_prediction_project
   ```

2. **Start the application**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - Health Check: http://localhost:5000/health

### Option 2: Manual Development Setup

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask server**
   ```bash
   cd app
   python app.py
   ```

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm start
   ```

## 📁 Project Structure

```
disease_prediction_project/
├── backend/
│   ├── app/
│   │   ├── app.py              # Flask application
│   │   └── models.py           # SQLAlchemy database models
│   ├── model/
│   │   ├── model_final.pkl     # Trained ML model
│   │   ├── scaler_final.pkl    # Feature scaler
│   │   ├── train_model.ipynb   # Model training notebook
│   │   └── load_heart_data.ipynb
│   ├── init_db.py              # Database initialization script
│   ├── Dockerfile              # Backend container config
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── PredictionForm.js    # Input form component
│   │   │   ├── PredictionForm.css
│   │   │   ├── ResultDisplay.js     # Results display component
│   │   │   ├── ResultDisplay.css
│   │   │   ├── HistoryPanel.js      # Prediction history component
│   │   │   └── HistoryPanel.css
│   │   ├── App.js              # Main application component
│   │   ├── App.css             # Main styles
│   │   ├── index.js            # React entry point
│   │   └── index.css           # Global styles
│   ├── public/
│   │   ├── index.html          # HTML template
│   │   └── manifest.json       # PWA manifest
│   ├── Dockerfile              # Frontend container config
│   ├── nginx.conf              # Nginx configuration
│   └── package.json            # Node.js dependencies
├── data/
│   ├── heart.csv              # Original dataset
│   └── heart_clean.csv        # Cleaned dataset
├── docker-compose.yml         # Multi-container configuration
└── README.md                  # Project documentation
```

## 🛠️ API Endpoints

### Backend API

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|--------------|----------|
| `/health` | GET | Health check | None | `{"status": "healthy", "model_loaded": true}` |
| `/features` | GET | Get feature information | None | Feature definitions and validation rules |
| `/predict` | POST | Predict heart disease risk | JSON with medical parameters | Risk assessment with prediction ID |
| `/history/<session_id>` | GET | Get user prediction history | None | User info and prediction history |
| `/stats` | GET | Get application statistics | None | Usage statistics and analytics |
| `/export/<session_id>` | GET | Export user data | None | Complete user data in JSON format |

### Example API Usage

```bash
# Health check
curl http://localhost:5000/health

# Get prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 63,
    "sex": 1,
    "cp": 1,
    "trestbps": 145,
    "chol": 233,
    "fbs": 1,
    "restecg": 2,
    "thalach": 150,
    "exang": 0,
    "oldpeak": 2.3,
    "slope": 3,
    "ca": 0,
    "thal": 6
  }'
```

## 🎨 UI/UX Features

- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Real-time Validation**: Instant feedback on form inputs with helpful error messages
- **Interactive Risk Meter**: Animated circular progress indicator showing risk percentage
- **Color-coded Risk Levels**: 
  - 🟢 Green (0-30%): Low Risk
  - 🟡 Yellow (30-70%): Moderate Risk
  - 🔴 Red (70-100%): High Risk
- **Professional Recommendations**: Tailored health advice based on risk level
- **Print Functionality**: Generate printable reports for medical records
- **Accessibility**: WCAG compliant with proper ARIA labels and keyboard navigation

## 🔒 Security Features

- **Input Validation**: Comprehensive client and server-side validation
- **CORS Configuration**: Properly configured cross-origin resource sharing
- **Security Headers**: XSS protection, content type options, and frame options
- **Non-root Container**: Backend runs with non-privileged user
- **Health Monitoring**: Built-in health checks for service monitoring

## 🧪 Model Information

- **Algorithm**: Logistic Regression with Standard Scaler
- **Dataset**: Heart Disease UCI dataset (303 samples, 14 features)
- **Performance**: Trained with 80/20 train-test split
- **Features**: All 13 medical parameters normalized using StandardScaler
- **Output**: Binary classification (0: No Disease, 1: Disease Present) with probability scores

## 🐳 Docker Configuration

### Backend Container
- **Base Image**: Python 3.9 Slim
- **Port**: 5000
- **Health Check**: GET /health endpoint
- **Security**: Non-root user execution

### Frontend Container
- **Build Stage**: Node.js 18 Alpine for building React app
- **Runtime Stage**: Nginx Alpine for serving static files
- **Port**: 80 (mapped to 3000 externally)
- **Features**: Gzip compression, security headers, client-side routing support

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `production` |
| `REACT_APP_API_URL` | Backend API URL | `http://localhost:5000` |

### Production Deployment

For production deployment, update the environment variables:

```yaml
environment:
  - REACT_APP_API_URL=https://your-backend-domain.com
```

## 🚨 Medical Disclaimer

⚠️ **IMPORTANT**: This application is for educational and demonstration purposes only. The predictions provided by this system should NOT be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical decisions.

## 📊 Performance Monitoring

The application includes built-in monitoring:

- **Health Checks**: Both services have health endpoints
- **Graceful Startup**: Frontend waits for backend to be healthy
- **Automatic Restarts**: Services restart unless manually stopped
- **Resource Optimization**: Multi-stage Docker builds for minimal image size

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check which process is using the port
   lsof -i :3000  # or :5000
   # Kill the process or use different ports in docker-compose.yml
   ```

2. **Model Files Missing**
   ```bash
   # Ensure model files exist in backend/model/
   ls -la backend/model/
   # Should show model_final.pkl and scaler_final.pkl
   ```

3. **Docker Build Fails**
   ```bash
   # Clean Docker cache and rebuild
   docker system prune -f
   docker-compose up --build --force-recreate
   ```

4. **CORS Issues**
   ```bash
   # Check if backend is running and accessible
   curl http://localhost:5000/health
   ```

### Logs

View application logs:
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the troubleshooting section above
- Review the API documentation

---

**Built with ❤️ using Flask, React, and Docker**