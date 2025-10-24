from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to predictions
    predictions = db.relationship('Prediction', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'created_at': self.created_at.isoformat(),
            'predictions_count': len(self.predictions)
        }

class Prediction(db.Model):
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Input features
    age = db.Column(db.Float, nullable=False)
    sex = db.Column(db.Float, nullable=False)
    cp = db.Column(db.Float, nullable=False)
    trestbps = db.Column(db.Float, nullable=False)
    chol = db.Column(db.Float, nullable=False)
    fbs = db.Column(db.Float, nullable=False)
    restecg = db.Column(db.Float, nullable=False)
    thalach = db.Column(db.Float, nullable=False)
    exang = db.Column(db.Float, nullable=False)
    oldpeak = db.Column(db.Float, nullable=False)
    slope = db.Column(db.Float, nullable=False)
    ca = db.Column(db.Float, nullable=False)
    thal = db.Column(db.Float, nullable=False)
    
    # Prediction results
    prediction = db.Column(db.Integer, nullable=False)  # 0 or 1
    risk_percentage = db.Column(db.Float, nullable=False)
    risk_level = db.Column(db.String(50), nullable=False)  # Low, Moderate, High
    confidence = db.Column(db.Float, nullable=False)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))  # Support IPv6
    user_agent = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'input_features': {
                'age': self.age,
                'sex': self.sex,
                'cp': self.cp,
                'trestbps': self.trestbps,
                'chol': self.chol,
                'fbs': self.fbs,
                'restecg': self.restecg,
                'thalach': self.thalach,
                'exang': self.exang,
                'oldpeak': self.oldpeak,
                'slope': self.slope,
                'ca': self.ca,
                'thal': self.thal
            },
            'prediction_results': {
                'prediction': self.prediction,
                'risk_percentage': self.risk_percentage,
                'risk_level': self.risk_level,
                'confidence': self.confidence
            },
            'created_at': self.created_at.isoformat(),
            'ip_address': self.ip_address
        }
    
    @classmethod
    def create_from_request(cls, user_id, input_data, prediction_results, request_info):
        """Create a prediction record from request data"""
        return cls(
            user_id=user_id,
            # Input features
            age=float(input_data['age']),
            sex=float(input_data['sex']),
            cp=float(input_data['cp']),
            trestbps=float(input_data['trestbps']),
            chol=float(input_data['chol']),
            fbs=float(input_data['fbs']),
            restecg=float(input_data['restecg']),
            thalach=float(input_data['thalach']),
            exang=float(input_data['exang']),
            oldpeak=float(input_data['oldpeak']),
            slope=float(input_data['slope']),
            ca=float(input_data['ca']),
            thal=float(input_data['thal']),
            # Prediction results
            prediction=prediction_results['prediction'],
            risk_percentage=prediction_results['risk_percentage'],
            risk_level=prediction_results['risk_level'],
            confidence=float(prediction_results['interpretation']['confidence'].rstrip('%')),
            # Metadata
            ip_address=request_info.get('ip_address'),
            user_agent=request_info.get('user_agent')
        )