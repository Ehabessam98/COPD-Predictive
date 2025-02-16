import streamlit as st
import joblib
import numpy as np

# Load the model, scaler, and label encoders
model = joblib.load("copd_asthma_model.pkl")
scaler = joblib.load("scaler.pkl")
label_encoders = joblib.load("label_encoders.pkl")

# Set page configuration
st.set_page_config(page_title="COPD-Asthma Prediction", page_icon="🔍", layout="wide")

# Custom CSS for a fancier UI
st.markdown(
    """
    <style>
        .stApp {
            background-color: #FAE3B4;
        }
        .sidebar .sidebar-content {
            background-color: #F4D03F;
        }
        h1 {
            color: #8B0000;
            text-align: center;
        }
        .prediction-result {
            font-size: 24px;
            font-weight: bold;
            color: #004080;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("🔬 COPD-Asthma Prediction App")

# Sidebar for user input
st.sidebar.header("📝 Enter Patient Information")
age = st.sidebar.slider("Age", 10, 90, 40)
peak_flow = st.sidebar.slider("Peak Flow (L/min)", 100, 700, 350)
smoking_status = st.sidebar.selectbox("Smoking Status", ["Never", "Former", "Current"])
persistent_cough = st.sidebar.selectbox("Persistent Cough", ["No", "Yes"])
family_history = st.sidebar.selectbox("Family History", ["No", "Yes"])

# Convert categorical values to numerical
if smoking_status in label_encoders["Smoking Status"].classes_:
    smoking_status_encoded = label_encoders["Smoking Status"].transform([smoking_status])[0]
else:
    smoking_status_encoded = -1  # Assign a default unknown label
persistent_cough_encoded = label_encoders["Persistent Cough"].transform([persistent_cough])[0]
family_history_encoded = label_encoders["Family History"].transform([family_history])[0]

# Prepare input data
input_data = np.array([[age, peak_flow, smoking_status_encoded, persistent_cough_encoded, family_history_encoded]])

# Scale the input data
input_data_scaled = scaler.transform(input_data)

# Make a prediction
prediction = model.predict(input_data_scaled)
predicted_condition = label_encoders["Condition"].inverse_transform(prediction)[0]

# Display prediction
st.subheader("📌 Prediction Result")
st.markdown(f'<p class="prediction-result">Predicted Condition: {predicted_condition}</p>', unsafe_allow_html=True)

# Additional model details
with st.expander("🔎 Model Details"):
    st.write("🔹 **Model Raw Prediction:**", prediction[0])
    st.write("🔹 **Prediction Probabilities:**")
    st.table(model.predict_proba(input_data_scaled))
    st.write("🔹 **Condition Class Labels:**")
    st.table(label_encoders["Condition"].classes_)

# Footer
st.markdown("""
    <hr>
    <p style='text-align: center;'>Created by <b>Ehab Essam</b></p>
    """, unsafe_allow_html=True)
