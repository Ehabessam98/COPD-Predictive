import streamlit as st
import numpy as np
import joblib
import plotly.graph_objects as go

# Load the trained COPD model
model = joblib.load("copd_prediction_model.pkl")

# Fancy UI Styling
st.set_page_config(page_title="COPD Risk Predictor", page_icon="💨", layout="centered")

st.title("💨 COPD Risk Prediction App")
st.write("Enter patient details below to predict the risk of COPD.")

# Sidebar with input fields
st.sidebar.header("📋 Patient Information")

age = st.sidebar.slider("Age", 30, 90, 55)
peak_flow = st.sidebar.slider("Peak Flow (L/min)", 150, 700, 400)
smoking_status = st.sidebar.radio("Smoking Status", ["Non-Smoker", "Smoker"])
persistent_cough = st.sidebar.radio("Persistent Cough", ["No", "Yes"])
family_history = st.sidebar.radio("Family History of COPD", ["No", "Yes"])

# Convert categorical inputs to numerical
smoking_status = 1 if smoking_status == "Smoker" else 0
persistent_cough = 1 if persistent_cough == "Yes" else 0
family_history = 1 if family_history == "Yes" else 0

# Prediction
input_data = np.array([[age, peak_flow, smoking_status, persistent_cough, family_history]])
prediction_proba = model.predict_proba(input_data)[0][1]  # Probability of COPD
prediction = "High Risk of COPD" if prediction_proba > 0.5 else "Low Risk of COPD"

# 🎨 Gauge Meter for Visual Risk Representation
fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=prediction_proba * 100,
    title={"text": "COPD Risk (%)"},
    gauge={
        "axis": {"range": [0, 100]},
        "bar": {"color": "red" if prediction_proba > 0.5 else "green"},
        "steps": [
            {"range": [0, 50], "color": "lightgreen"},
            {"range": [50, 75], "color": "yellow"},
            {"range": [75, 100], "color": "red"}
        ],
    }
))

# Display Prediction Result
st.subheader("🩺 Prediction Result")
st.markdown(f"**{prediction}** (Probability: {prediction_proba:.2%})")
st.plotly_chart(fig)

# Footer - Centered Below the Graph
st.markdown(
    """
    <div style="text-align: center; margin-top: 20px; font-size: 16px; font-weight: bold;">
         Created By: <span style="color: grey;">Ehab Essam</span> 
    </div>
    """,
    unsafe_allow_html=True
)
