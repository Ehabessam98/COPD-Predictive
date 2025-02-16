import streamlit as st
import joblib
import numpy as np

# Load the model, scaler, and label encoders
model = joblib.load("copd_asthma_model.pkl")
scaler = joblib.load("scaler.pkl")
label_encoders = joblib.load("label_encoders.pkl")

# Define input fields
st.title("COPD-Asthma Prediction App")

st.sidebar.header("Enter Patient Information")
age = st.sidebar.slider("Age", 10, 90, 40)
peak_flow = st.sidebar.slider("Peak Flow (L/min)", 100, 700, 350)
smoking_status = st.sidebar.selectbox("Smoking Status", ["Never", "Quit", "Current"])
persistent_cough = st.sidebar.selectbox("Persistent Cough", ["No", "Yes"])
family_history = st.sidebar.selectbox("Family History", ["No", "Yes"])

# Convert categorical values to numerical using label encoders
try:
    smoking_status_encoded = label_encoders["Smoking Status"].transform([smoking_status])[0]
    persistent_cough_encoded = label_encoders["Persistent Cough"].transform([persistent_cough])[0]
    family_history_encoded = label_encoders["Family History"].transform([family_history])[0]
except KeyError as e:
    st.error(f"Encoding error: {e}")
    st.stop()

# Prepare input data
input_data = np.array([[age, peak_flow, smoking_status_encoded, persistent_cough_encoded, family_history_encoded]])

# Scale the input data
input_data_scaled = scaler.transform(input_data)

# Make a prediction
prediction = model.predict(input_data_scaled)
predicted_condition = label_encoders["Condition"].inverse_transform(prediction)[0]

# Set color for prediction
color = "green" if predicted_condition == "Normal" else "grey" if predicted_condition == "Asthma" else "red"

# Display prediction with formatting
st.subheader("Prediction Result")
st.markdown(f"""
    <div style="background-color:{color}; padding:15px; border-radius:10px; text-align:center; font-size:24px; color:white;">
        <strong>Predicted Condition: {predicted_condition}</strong>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>Created by <strong>Ehab Essam</strong>", unsafe_allow_html=True)
