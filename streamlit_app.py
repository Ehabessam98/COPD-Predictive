import streamlit as st
import joblib
import numpy as np

# Load the model, scaler, and label encoders
model = joblib.load("copd_asthma_model.pkl")
scaler = joblib.load("scaler.pkl")
label_encoders = joblib.load("label_encoders.pkl")

# Define a function to safely encode categorical variables
def safe_encode(label_enc, value):
    """Safely encode labels, assigning unknown values to the first known class."""
    if value in label_enc.classes_:
        return label_enc.transform([value])[0]
    else:
        return label_enc.transform([label_enc.classes_[0]])[0]  # Assign to first known class

# Streamlit UI
st.title("COPD-Asthma Prediction App")

st.sidebar.header("Enter Patient Information")
age = st.sidebar.slider("Age", 10, 90, 40)
peak_flow = st.sidebar.slider("Peak Flow (L/min)", 100, 700, 350)
smoking_status = st.sidebar.selectbox("Smoking Status", label_encoders["Smoking Status"].classes_)
persistent_cough = st.sidebar.selectbox("Persistent Cough", label_encoders["Persistent Cough"].classes_)
family_history = st.sidebar.selectbox("Family History", label_encoders["Family History"].classes_)

# Encode categorical inputs safely
smoking_status_encoded = safe_encode(label_encoders["Smoking Status"], smoking_status)
persistent_cough_encoded = safe_encode(label_encoders["Persistent Cough"], persistent_cough)
family_history_encoded = safe_encode(label_encoders["Family History"], family_history)

# Prepare and scale input data
input_data = np.array([[age, peak_flow, smoking_status_encoded, persistent_cough_encoded, family_history_encoded]])
input_data_scaled = scaler.transform(input_data)

# Make a prediction
prediction = model.predict(input_data_scaled)
predicted_condition = label_encoders["Condition"].inverse_transform(prediction)[0]

# Display prediction
st.subheader("Prediction Result")
st.write(f"**Predicted Condition:** {predicted_condition}")
