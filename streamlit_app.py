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
smoking_status = st.sidebar.selectbox("Smoking Status", ["Never", "Former", "Current"])
persistent_cough = st.sidebar.selectbox("Persistent Cough", ["No", "Yes"])
family_history = st.sidebar.selectbox("Family History", ["No", "Yes"])

# Function to safely encode labels
def safe_encode(label_enc, value, default=0):
    """Safely encode a label, returning a default if the value is not in training data."""
    return label_enc.transform([value])[0] if value in label_enc.classes_ else default

# Convert categorical values to numerical
smoking_status_encoded = safe_encode(label_encoders["Smoking Status"], smoking_status)
persistent_cough_encoded = safe_encode(label_encoders["Persistent Cough"], persistent_cough)
family_history_encoded = safe_encode(label_encoders["Family History"], family_history)

# Prepare input data
input_data = np.array([[age, peak_flow, smoking_status_encoded, persistent_cough_encoded, family_history_encoded]])

# Check feature shape before scaling
expected_features = scaler.n_features_in_
if input_data.shape[1] != expected_features:
    st.error(f"Feature mismatch: Expected {expected_features}, but got {input_data.shape[1]}. Please retrain the model with the correct features.")
else:
   # Scale the input data
input_data_scaled = scaler.transform(input_data)

# Debugging: Print scaled input data
st.write("🔍 Scaled Input Data:", input_data_scaled)

# Make a prediction
prediction = model.predict(input_data_scaled)

# Debugging: Print model's raw prediction output
st.write("🔍 Model Raw Prediction:", prediction)

# Check probability scores for each condition
probabilities = model.predict_proba(input_data_scaled)
st.write("🔍 Prediction Probabilities:", probabilities)

# Convert predicted label back to condition name
predicted_condition = label_encoders["Condition"].inverse_transform(prediction)[0]

# Display prediction
st.subheader("Prediction Result")
st.write(f"**Predicted Condition:** {predicted_condition}")


# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>Created by Ehab Essam</p>", unsafe_allow_html=True)
