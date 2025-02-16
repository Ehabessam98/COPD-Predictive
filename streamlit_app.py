import streamlit as st
import joblib
import numpy as np

# Load the model, scaler, and label encoders
model = joblib.load("copd_asthma_model.pkl")
scaler = joblib.load("scaler.pkl")
label_encoders = joblib.load("label_encoders.pkl")

# Set page configuration
st.set_page_config(page_title="COPD & Asthma Prediction", page_icon="🫁", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
        body {
            background-color: #F4F6F7;
        }
        .stApp {
            background-color: #F8F9FA;
        }
        .main-container {
            max-width: 700px;
            margin: auto;
            padding: 30px;
            background-color: white;
            border-radius: 12px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #2C3E50;
            text-align: center;
        }
        .header-text {
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            color: #34495E;
            margin-bottom: 10px;
        }
        .stButton>button {
            background-color: #3498DB;
            color: white;
            font-size: 18px;
            padding: 10px 20px;
            border-radius: 8px;
        }
        .stButton>button:hover {
            background-color: #2980B9;
        }
        .prediction-box {
            text-align: center;
            background-color: #2ECC71;
            color: white;
            font-size: 24px;
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

# Centered main container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# New title header for "PFA - Digital Transformation"
st.markdown('<p class="header-text">PFA - Digital Transformation</p>', unsafe_allow_html=True)

# Updated Title with Proper Emoji
st.title("🫁 COPD & Asthma Prediction")

# Sidebar for user input
st.sidebar.header("📋 Patient Information")
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

# Close main container
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <hr>
    <p style='text-align: center; color: gray;'>Created by <b>Ehab Essam</b></p>
    """, unsafe_allow_html=True)
