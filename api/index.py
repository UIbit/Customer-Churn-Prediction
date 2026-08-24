from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import pickle
import pandas as pd
import numpy as np
from typing import List
import os

app = FastAPI(title="ApexPulse Churn Prediction API", version="1.0.0")

# Load models
def load_models():
    try:
        model = pickle.load(open("models/best_model.pkl", "rb"))
        scaler = pickle.load(open("models/scaler.pkl", "rb"))
        le_geo = pickle.load(open("models/le_geo.pkl", "rb"))
        le_gen = pickle.load(open("models/le_gen.pkl", "rb"))
        features = pickle.load(open("models/feature_names.pkl", "rb"))
        return model, scaler, le_geo, le_gen, features
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading models: {str(e)}")

model, scaler, le_geo, le_gen, feature_names = load_models()

class CustomerProfile(BaseModel):
    credit_score: int
    geography: str
    gender: str
    age: int
    tenure: int
    balance: float
    num_products: int
    has_cr_card: str
    is_active: str
    estimated_salary: float

class PredictionResponse(BaseModel):
    churn_probability: float
    churn_prediction: int
    risk_level: str
    confidence: float
    recommendations: List[str]

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ApexPulse Churn Prediction API</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .container { max-width: 800px; margin: 0 auto; background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; backdrop-filter: blur(10px); }
            h1 { text-align: center; margin-bottom: 30px; }
            .endpoint { background: rgba(255,255,255,0.2); padding: 20px; margin: 15px 0; border-radius: 10px; }
            .method { background: #28a745; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; }
            code { background: rgba(0,0,0,0.3); padding: 2px 6px; border-radius: 4px; }
            a { color: #ffd700; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏦 ApexPulse Churn Prediction API</h1>
            <p>Machine Learning-powered customer churn prediction for banking institutions.</p>
            
            <div class="endpoint">
                <h3><span class="method">POST</span> /predict</h3>
                <p>Predict customer churn probability and get actionable recommendations.</p>
                <p><strong>Try it:</strong> <a href="/docs" target="_blank">Interactive API Documentation</a></p>
            </div>

            <div class="endpoint">
                <h3><span class="method">GET</span> /health</h3>
                <p>Check API health status and model information.</p>
            </div>

            <div class="endpoint">
                <h3>🔗 Links</h3>
                <ul>
                    <li><a href="/docs" target="_blank">📚 API Documentation (Swagger)</a></li>
                    <li><a href="/redoc" target="_blank">📖 Alternative Documentation (ReDoc)</a></li>
                    <li><a href="https://github.com/UIbit/Customer-Churn-Prediction" target="_blank">💻 GitHub Repository</a></li>
                </ul>
            </div>

            <div class="endpoint">
                <h3>💡 About</h3>
                <p>This API uses a Random Forest model with 86.6% accuracy to predict customer churn based on demographic and account features. Perfect for integration into banking CRM systems and customer retention workflows.</p>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "model_type": "Random Forest",
        "accuracy": "86.6%",
        "features_count": len(feature_names),
        "api_version": "1.0.0"
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict_churn(profile: CustomerProfile):
    try:
        # Encode categorical variables
        geo_enc = le_geo.transform([profile.geography])[0]
        gen_enc = le_gen.transform([profile.gender])[0]
        cr_card = 1 if profile.has_cr_card.lower() == "yes" else 0
        active = 1 if profile.is_active.lower() == "yes" else 0

        # Create feature vector
        features = pd.DataFrame([[
            profile.credit_score, geo_enc, gen_enc, profile.age, profile.tenure,
            profile.balance, profile.num_products, cr_card, active, profile.estimated_salary
        ]], columns=feature_names)

        # Make prediction
        scaled_features = scaler.transform(features)
        churn_prob = model.predict_proba(scaled_features)[0][1]
        churn_pred = model.predict(scaled_features)[0]
        
        # Determine risk level and recommendations
        risk_level = "HIGH" if churn_pred == 1 else "LOW"
        confidence = max(churn_prob, 1 - churn_prob)
        
        if churn_pred == 1:
            recommendations = [
                "Contact customer immediately via relationship manager",
                "Offer personalized rate revision or fee waiver", 
                "Present additional product bundling options",
                "Schedule satisfaction review call within 48 hours"
            ]
        else:
            recommendations = [
                "Focus on upselling premium products",
                "Enroll customer in loyalty rewards program",
                "Offer investment or wealth management consultation",
                "Maintain regular quarterly check-ins"
            ]

        return PredictionResponse(
            churn_probability=float(churn_prob),
            churn_prediction=int(churn_pred),
            risk_level=risk_level,
            confidence=float(confidence),
            recommendations=recommendations
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@app.get("/countries")
async def get_countries():
    """Get available countries for geography field"""
    return {"countries": list(le_geo.classes_)}

@app.get("/genders") 
async def get_genders():
    """Get available genders"""
    return {"genders": list(le_gen.classes_)}

# Error handler for model loading issues
@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"error": "Internal server error", "detail": "Model loading failed"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)