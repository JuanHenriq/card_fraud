import joblib
import os

model_path = os.path.join(os.path.dirname(__file__), '../card_fraud_model.pkl')
model = joblib.load(model_path)