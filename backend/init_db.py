#!/usr/bin/env python3
"""
Database initialization script for Heart Disease Prediction App
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent / 'app'
sys.path.insert(0, str(app_dir))

from app import app, db
from models import User, Prediction

def init_database():
    """Initialize the database with tables"""
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Print table information
            print("\n📊 Created tables:")
            print("- users: Store user sessions")
            print("- predictions: Store prediction inputs and results")
            
            # Check if tables exist
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"\n📋 Available tables: {tables}")
            
        except Exception as e:
            print(f"❌ Error creating database: {e}")
            return False
    
    return True

def create_sample_data():
    """Create some sample data for testing"""
    with app.app_context():
        try:
            # Check if we already have data
            if User.query.count() > 0:
                print("📝 Sample data already exists, skipping...")
                return
            
            # Create a sample user
            sample_user = User(session_id="sample-session-123")
            db.session.add(sample_user)
            db.session.flush()  # Get the ID
            
            # Create a sample prediction
            sample_prediction = Prediction(
                user_id=sample_user.id,
                age=45.0,
                sex=1.0,
                cp=2.0,
                trestbps=130.0,
                chol=200.0,
                fbs=0.0,
                restecg=0.0,
                thalach=150.0,
                exang=0.0,
                oldpeak=1.5,
                slope=2.0,
                ca=0.0,
                thal=3.0,
                prediction=0,
                risk_percentage=25.5,
                risk_level="Low",
                confidence=89.5,
                ip_address="127.0.0.1",
                user_agent="Sample User Agent"
            )
            
            db.session.add(sample_prediction)
            db.session.commit()
            
            print("✅ Sample data created successfully!")
            
        except Exception as e:
            print(f"❌ Error creating sample data: {e}")
            db.session.rollback()

if __name__ == "__main__":
    print("🚀 Initializing Heart Disease Prediction Database...")
    
    if init_database():
        print("\n🎯 Database initialization completed!")
        
        # Optionally create sample data
        create_sample_data()
        
        print("\n🔗 Database connection string:")
        print(f"   {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        print("\n📖 Available API endpoints:")
        print("   GET  /health              - Health check")
        print("   GET  /features            - Feature information")
        print("   POST /predict             - Make prediction")
        print("   GET  /history/<session>   - Get user history")
        print("   GET  /stats               - Get app statistics")
        print("   GET  /export/<session>    - Export user data")
        
    else:
        print("❌ Database initialization failed!")
        sys.exit(1)