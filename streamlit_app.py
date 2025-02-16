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
smoking_status = st.sidebar.selectbox("Smoking Status", list(label_encoders["Smoking Status"].classes_))
persistent_cough = st.sidebar.selectbox("Persistent Cough", list(label_encoders["Persistent Cough"].classes_))
family_history = st.sidebar.selectbox("Family History", list(label_encoders["Family History"].classes_))

# Function to encode categorical values
def encode_feature(feature_name, value):
    return label_encoders[feature_name].transform([value])[0]

# Convert categorical values to numerical using label encoders
smoking_status_encoded = encode_feature("Smoking Status", smoking_status)
persistent_cough_encoded = encode_feature("Persistent Cough", persistent_cough)
family_history_encoded = encode_feature("Family History", family_history)

# Prepare input data
input_data = np.array([[age, peak_flow, smoking_status_encoded, persistent_cough_encoded, family_history_encoded]])

# Scale the input data
input_data_scaled = scaler.transform(input_data)

# Make a prediction
prediction = model.predict(input_data_scaled)
predicted_condition = label_encoders["Condition"].inverse_transform(prediction)[0]

# Determine if the patient is Normal or has COPD/Asthma
if predicted_condition == "Normal" and peak_flow >= (400 - (age * 2)) and persistent_cough == "No" and family_history == "No":
    final_condition = "Normal (Healthy)"
    color = "darkgreen"
else:
    final_condition = "COPD or Asthma"
    color = "darkred"

# Display prediction with formatting
st.subheader("Prediction Result")
st.markdown(f"""
    <div style="background-color:{color}; padding:15px; border-radius:10px; text-align:center; font-size:24px; color:white;">
        <strong>Predicted Condition: {final_condition}</strong>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>Created by <strong>Ehab Essam</strong>", unsafe_allow_html=True)
