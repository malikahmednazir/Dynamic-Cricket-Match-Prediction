# Dynamic Cricket Match Prediction

Angular frontend and Python Flask API.

## Frontend
cd frontend
npm install
npm start

## Backend
cd backend
pip install -r requirements.txt
python app.py

Backend health: http://localhost:5000/api/health

## Deployment
Frontend: Vercel (root directory: frontend)
Backend: Render (use render.yaml)

The trained machine learning model must be connected before
real match predictions can be returned.
