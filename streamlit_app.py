import streamlit as st
from PIL import Image

def classify_condition(age, peak_flow, smoking_status, persistent_cough, family_history):
    """
    Classify the condition based on peak flow and risk factors.
    """
    # Predicted normal peak flow based on an assumed reference (adjust for real cases)
    predicted_normal = 600  # Example for an adult, should be dynamic
    
    # Define ranges
    healthy_range = (400, 700)  # Healthy adults
    copd_mild_range = (0.5 * predicted_normal, 0.8 * predicted_normal)
    copd_moderate_range = (0.3 * predicted_normal, 0.5 * predicted_normal)
    copd_severe_threshold = 0.3 * predicted_normal
    asthma_mild_threshold = 0.5 * predicted_normal
    asthma_normal_range = (0.8 * predicted_normal, predicted_normal)
    
    # Condition Classification
    if healthy_range[0] <= peak_flow <= healthy_range[1] and smoking_status == "Never" and persistent_cough == "No":
        return "Healthy", "green"
    elif peak_flow < copd_severe_threshold or (smoking_status in ["Former", "Current"] and peak_flow <= copd_moderate_range[1]):
        return "COPD", "red"
    elif asthma_mild_threshold <= peak_flow <= asthma_normal_range[1]:
        return "Asthma", "blue"
    else:
        return "Uncertain", "gray"

# Streamlit UI
st.set_page_config(layout="wide")
st.title("\U0001F5A8 COPD & Asthma Prediction")  # Adding a lung symbol

# Sidebar for patient input
st.sidebar.header("\U0001F4DD Patient Information")
age = st.sidebar.slider("Age", 10, 90, 35)
peak_flow = st.sidebar.slider("Peak Flow (L/min)", 100, 700, 479)
smoking_status = st.sidebar.selectbox("Smoking Status", ["Never", "Former", "Current"])
persistent_cough = st.sidebar.selectbox("Persistent Cough", ["No", "Yes"])
family_history = st.sidebar.selectbox("Family History", ["No", "Yes"])

# Classification
condition, color = classify_condition(age, peak_flow, smoking_status, persistent_cough, family_history)

# Display prediction
st.markdown("""
    <div style="text-align: center; font-size: 20px;">
        <strong>PFA - Digital Transformation</strong>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div style="background-color:{color}; padding:15px; border-radius:10px; text-align:center; font-size:24px; color:white;">
        <strong>Predicted Condition: {condition}</strong>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>Created by <strong>Ehab Essam</strong>", unsafe_allow_html=True)
