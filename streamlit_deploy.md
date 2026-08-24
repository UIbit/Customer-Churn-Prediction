# Streamlit Cloud Deployment Guide

## Quick Deployment to Streamlit Cloud

1. **Go to**: https://share.streamlit.io/
2. **Sign in** with your GitHub account
3. **Click "New app"**
4. **Select your repository**: UIbit/Customer-Churn-Prediction
5. **Set main file path**: `app.py`
6. **Deploy!**

Your app will be available at:
`https://uibit-customer-churn-prediction-app-xyz123.streamlit.app/`

## Benefits of Streamlit Cloud:
✅ Free hosting for public repos
✅ Automatic builds from GitHub
✅ Built-in Streamlit runtime
✅ HTTPS by default
✅ Custom domain support
✅ No configuration needed

## Alternative: Railway.app
1. Go to https://railway.app/
2. Connect GitHub repo
3. Select Python template
4. Add start command: `streamlit run app.py --server.port $PORT`
5. Deploy