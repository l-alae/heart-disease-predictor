from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_migrate import Migrate
import joblib
import numpy as np
import pandas as pd
import os
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from models import db, User, Prediction

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:3000'])

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 
    'postgresql://postgres:password@postgres:5432/heart_prediction'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')

# Initialize database
db.init_app(app)
migrate = Migrate(app, db)

# Get the directory of the current file
current_dir = Path(__file__).parent
model_dir = current_dir.parent / "model"

print(f"🔍 Current directory: {current_dir}")
print(f"🔍 Looking for models in: {model_dir}")
print(f"🔍 Model directory exists: {model_dir.exists()}")
if model_dir.exists():
    print(f"🔍 Files in model directory: {list(model_dir.iterdir())}")

# Load the trained model and scaler
model = None
scaler = None

# Try different possible paths for the model files
possible_paths = [
    model_dir,  # /app/model (from volume mount)
    Path("/app/model"),  # Direct path
    current_dir / "../model",  # Relative path
    Path("./model"),  # Current working directory
]

for path in possible_paths:
    try:
        print(f"🔍 Trying path: {path}")
        if path.exists():
            print(f"🔍 Path exists, files: {list(path.iterdir())}")
            model_file = path / "model_final.pkl"
            scaler_file = path / "scaler_final.pkl"
            
            if model_file.exists() and scaler_file.exists():
                try:
                    model = joblib.load(model_file)
                    print(f"✅ Model loaded successfully from: {model_file}")
                except Exception as e:
                    print(f"❌ Error loading model from {model_file}: {e}")
                    continue
                
                try:
                    scaler = joblib.load(scaler_file)
                    print(f"✅ Scaler loaded successfully from: {scaler_file}")
                except Exception as e:
                    print(f"❌ Error loading scaler from {scaler_file}: {e}")
                    model = None  # Reset model if scaler fails
                    continue
                
                if model is not None and scaler is not None:
                    print(f"✅ Both model and scaler loaded successfully from: {path}")
                    break
            else:
                missing = []
                if not model_file.exists():
                    missing.append("model_final.pkl")
                if not scaler_file.exists():
                    missing.append("scaler_final.pkl")
                print(f"❌ Missing files in {path}: {missing}")
        else:
            print(f"❌ Path does not exist: {path}")
    except Exception as e:
        print(f"❌ Error loading from {path}: {e}")

if model is None or scaler is None:
    print("❌ Failed to load model and scaler from all possible paths")

# Database helper functions
def get_or_create_user(session_id=None):
    """Get existing user or create new one"""
    if not session_id:
        session_id = str(uuid.uuid4())
    
    user = User.query.filter_by(session_id=session_id).first()
    if not user:
        user = User(session_id=session_id)
        db.session.add(user)
        db.session.commit()
        print(f"✅ Created new user with session_id: {session_id}")
    
    return user

def save_prediction(user_id, input_data, prediction_results, request_info):
    """Save prediction to database"""
    try:
        prediction_record = Prediction.create_from_request(
            user_id=user_id,
            input_data=input_data,
            prediction_results=prediction_results,
            request_info=request_info
        )
        
        db.session.add(prediction_record)
        db.session.commit()
        print(f"✅ Saved prediction record with ID: {prediction_record.id}")
        return prediction_record
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error saving prediction: {e}")
        return None

# Create tables on startup
def create_tables():
    """Create database tables"""
    try:
        with app.app_context():
            db.create_all()
            print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")

# Initialize database on startup
create_tables()

# Feature names in the same order as training data
FEATURE_NAMES = [
    'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 
    'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
]

# Feature descriptions for better UX
FEATURE_INFO = {
    'age': {'name': 'Age', 'unit': 'years', 'min': 1, 'max': 120},
    'sex': {'name': 'Sex', 'options': {'1': 'Male', '0': 'Female'}},
    'cp': {'name': 'Chest Pain Type', 'options': {
        '1': 'Typical Angina',
        '2': 'Atypical Angina', 
        '3': 'Non-Anginal Pain',
        '4': 'Asymptomatic'
    }},
    'trestbps': {'name': 'Resting Blood Pressure', 'unit': 'mm Hg', 'min': 80, 'max': 200},
    'chol': {'name': 'Cholesterol', 'unit': 'mg/dl', 'min': 100, 'max': 600},
    'fbs': {'name': 'Fasting Blood Sugar > 120 mg/dl', 'options': {'1': 'True', '0': 'False'}},
    'restecg': {'name': 'Resting ECG Results', 'options': {
        '0': 'Normal',
        '1': 'ST-T Wave Abnormality',
        '2': 'Left Ventricular Hypertrophy'
    }},
    'thalach': {'name': 'Maximum Heart Rate Achieved', 'unit': 'bpm', 'min': 60, 'max': 220},
    'exang': {'name': 'Exercise Induced Angina', 'options': {'1': 'Yes', '0': 'No'}},
    'oldpeak': {'name': 'ST Depression Induced by Exercise', 'unit': 'mm', 'min': 0, 'max': 10},
    'slope': {'name': 'Slope of Peak Exercise ST Segment', 'options': {
        '1': 'Upsloping',
        '2': 'Flat',
        '3': 'Downsloping'
    }},
    'ca': {'name': 'Number of Major Vessels Colored by Fluoroscopy', 'options': {
        '0': '0', '1': '1', '2': '2', '3': '3'
    }},
    'thal': {'name': 'Thalassemia', 'options': {
        '3': 'Normal',
        '6': 'Fixed Defect',
        '7': 'Reversible Defect'
    }}
}

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'scaler_loaded': scaler is not None
    })

@app.route('/features', methods=['GET'])
def get_features():
    """Get feature information for the frontend"""
    return jsonify({
        'features': FEATURE_INFO,
        'feature_order': FEATURE_NAMES
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Predict heart disease risk"""
    try:
        if model is None or scaler is None:
            return jsonify({
                'error': 'Model or scaler not loaded properly'
            }), 500

        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No data provided'
            }), 400

        # Validate that all required features are present
        missing_features = [f for f in FEATURE_NAMES if f not in data]
        if missing_features:
            return jsonify({
                'error': f'Missing required features: {missing_features}'
            }), 400

        # Extract features in the correct order
        features = []
        for feature_name in FEATURE_NAMES:
            value = data[feature_name]
            try:
                features.append(float(value))
            except (ValueError, TypeError):
                return jsonify({
                    'error': f'Invalid value for {feature_name}: {value}'
                }), 400

        # Convert to numpy array and reshape for prediction
        features_array = np.array(features).reshape(1, -1)
        
        # Scale the features
        features_scaled = scaler.transform(features_array)
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        prediction_proba = model.predict_proba(features_scaled)[0]
        
        # Calculate risk percentage
        risk_percentage = float(prediction_proba[1] * 100)  # Probability of positive class
        
        # Determine risk level
        if risk_percentage < 30:
            risk_level = "Low"
            risk_color = "#28a745"  # Green
        elif risk_percentage < 70:
            risk_level = "Moderate"
            risk_color = "#ffc107"  # Yellow
        else:
            risk_level = "High"
            risk_color = "#dc3545"  # Red

        # Prepare response
        response_data = {
            'prediction': int(prediction),
            'risk_percentage': round(risk_percentage, 2),
            'risk_level': risk_level,
            'risk_color': risk_color,
            'interpretation': {
                'result': 'Heart Disease Detected' if prediction == 1 else 'No Heart Disease Detected',
                'confidence': f'{round(max(prediction_proba) * 100, 2)}%',
                'recommendation': get_recommendation(risk_percentage)
            }
        }

        # Save to database
        try:
            # Get or create user based on session
            session_id = request.headers.get('X-Session-ID') or str(uuid.uuid4())
            user = get_or_create_user(session_id)
            
            # Prepare request info
            request_info = {
                'ip_address': request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr),
                'user_agent': request.headers.get('User-Agent', '')
            }
            
            # Save prediction
            prediction_record = save_prediction(user.id, data, response_data, request_info)
            
            if prediction_record:
                response_data['prediction_id'] = prediction_record.id
                response_data['session_id'] = session_id
            
        except Exception as e:
            print(f"❌ Database error (continuing without saving): {e}")
            # Continue without database save if there's an error

        return jsonify(response_data)

    except Exception as e:
        return jsonify({
            'error': f'Prediction failed: {str(e)}'
        }), 500

def get_recommendation(risk_percentage):
    """Get health recommendation based on risk percentage"""
    if risk_percentage < 30:
        return "Your heart health appears good. Continue maintaining a healthy lifestyle with regular exercise and balanced diet."
    elif risk_percentage < 70:
        return "Moderate risk detected. Consider consulting with a healthcare provider for preventive measures and regular monitoring."
    else:
        return "High risk detected. Please consult with a cardiologist immediately for comprehensive evaluation and treatment planning."

@app.route('/history/<session_id>', methods=['GET'])
def get_user_history(session_id):
    """Get prediction history for a user"""
    try:
        user = User.query.filter_by(session_id=session_id).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        predictions = Prediction.query.filter_by(user_id=user.id).order_by(Prediction.created_at.desc()).all()
        
        return jsonify({
            'user': user.to_dict(),
            'predictions': [pred.to_dict() for pred in predictions]
        })
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve history: {str(e)}'}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get application statistics"""
    try:
        total_users = User.query.count()
        total_predictions = Prediction.query.count()
        
        # Risk level distribution
        risk_stats = db.session.query(
            Prediction.risk_level,
            db.func.count(Prediction.id).label('count')
        ).group_by(Prediction.risk_level).all()
        
        risk_distribution = {risk: count for risk, count in risk_stats}
        
        # Recent predictions (last 24 hours)
        recent_predictions = Prediction.query.filter(
            Prediction.created_at >= datetime.utcnow() - timedelta(days=1)
        ).count()
        
        return jsonify({
            'total_users': total_users,
            'total_predictions': total_predictions,
            'recent_predictions_24h': recent_predictions,
            'risk_distribution': risk_distribution
        })
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve stats: {str(e)}'}), 500

@app.route('/export/<session_id>', methods=['GET'])
def export_user_data(session_id):
    """Export user data in JSON format"""
    try:
        user = User.query.filter_by(session_id=session_id).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        predictions = Prediction.query.filter_by(user_id=user.id).order_by(Prediction.created_at.desc()).all()
        
        export_data = {
            'user_info': user.to_dict(),
            'predictions': [pred.to_dict() for pred in predictions],
            'export_timestamp': datetime.utcnow().isoformat(),
            'total_predictions': len(predictions)
        }
        
        return jsonify(export_data)
    except Exception as e:
        return jsonify({'error': f'Failed to export data: {str(e)}'}), 500

if __name__ == '__main__':
    print("🚀 Starting Flask app in debug mode...")
    app.run(debug=True, host='0.0.0.0', port=5000)