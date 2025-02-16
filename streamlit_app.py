import streamlit as st
import joblib
import numpy as np

# Load the model, scaler, and label encoders
model = joblib.load("copd_asthma_model.pkl")
scaler = joblib.load("scaler.pkl")
label_encoders = joblib.load("label_encoders.pkl")

# Set page configuration
st.set_page_config(page_title="COPD-Asthma Prediction", page_icon="🫁", layout="centered")

# Custom CSS for a modern UI
st.markdown(
    """
    <style>
        body {
            background-color: #FAE3B4;
        }
        .stApp {
            background-color: #FFF3E0;
            padding: 20px;
            border-radius: 15px;
            max-width: 700px;
            margin: auto;
        }
        h1 {
            color: #8B0000;
            text-align: center;
        }
        .stButton>button {
            background-color: #E74C3C;
            color: white;
            font-size: 18px;
            padding: 10px 20px;
            border-radius: 10px;
        }
        .stButton>button:hover {
            background-color: #C0392B;
        }
        .prediction-box {
            text-align: center;
            background-color: #2ECC71;
            color: white;
            font-size: 22px;
            font-weight: bold;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
        }
        footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("🫁 COPD & Asthma Prediction")

# Sidebar for user input
st.sidebar.header("📝 Enter Patient Information")
age = st.sidebar.slider("Age", 10, 90, 40)
peak_flow = st.sidebar.slider("Peak Flow (L/min)", 100, 700, 350)
smoking_status = st.sidebar.selectbox("Smoking Status", ["Never", "Former", "Current"])
persistent_cough = st.sidebar.selectbox("Persistent Cough", ["No", "Yes"])
family_history = st.sidebar.selectbox("Family History", ["No", "Yes"])

# Convert categorical values to numerical
def encode_feature(feature, encoder):
    return encoder.transform([feature])[0] if feature in encoder.classes_ else -1

smoking_status_encoded = encode_feature(smoking_status, label_encoders["Smoking Status"])
persistent_cough_encoded = encode_feature(persistent_cough, label_encoders["Persistent Cough"])
family_history_encoded = encode_feature(family_history, label_encoders["Family History"])

# Prepare input data
input_data = np.array([[age, peak_flow, smoking_status_encoded, persistent_cough_encoded, family_history_encoded]])
input_data_scaled = scaler.transform(input_data)

# Make a prediction
prediction = model.predict(input_data_scaled)
predicted_condition = label_encoders["Condition"].inverse_transform(prediction)[0]

# Display prediction result
st.markdown(f'<div class="prediction-box">Predicted Condition: {predicted_condition}</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <hr>
    <p style='text-align: center; color: gray;'>Created by <b>Ehab Essam</b></p>
    """, unsafe_allow_html=True)
