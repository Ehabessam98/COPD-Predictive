import streamlit as st

# Function to determine color based on prediction
def get_prediction_color(prediction):
    if prediction == "Healthy":
        return "green"
    elif prediction == "COPD":
        return "red"
    elif prediction == "Asthma":
        return "yellow"
    return "gray"

# Streamlit App
st.set_page_config(page_title="COPD & Asthma Prediction", layout="wide")

# Title and Header
st.markdown("<h3 style='text-align: center; font-weight: bold;'>PFA - Digital Transformation</h3>", unsafe_allow_html=True)

st.markdown(
    """
    <div style="text-align: center;">
        <h1>🫁 COPD & Asthma Prediction</h1>
    </div>
    """, 
    unsafe_allow_html=True
)

# Sidebar - Patient Information
st.sidebar.header("📋 Patient Information")

age = st.sidebar.slider("Age", 10, 90, 30)
peak_flow = st.sidebar.slider("Peak Flow (L/min)", 100, 700, 400)
smoking_status = st.sidebar.selectbox("Smoking Status", ["Never", "Former", "Current"])
persistent_cough = st.sidebar.selectbox("Persistent Cough", ["No", "Yes"])
family_history = st.sidebar.selectbox("Family History", ["No", "Yes"])

# Dummy Model Prediction Logic (Replace with real model)
if peak_flow > 500 and smoking_status == "Never" and persistent_cough == "No":
    prediction = "Healthy"
elif peak_flow < 250 or (smoking_status == "Current" and persistent_cough == "Yes"):
    prediction = "COPD"
else:
    prediction = "Asthma"

# Predicted Condition Display
color = get_prediction_color(prediction)

st.markdown(
    f"""
    <div style="text-align: center; padding: 10px; background-color: {color}; color: white; border-radius: 10px; font-size: 20px;">
        <strong>Predicted Condition: {prediction}</strong>
    </div>
    """,
    unsafe_allow_html=True
)

# Footer
st.markdown("<p style='text-align: center;'>Created by <strong>Ehab Essam</strong></p>", unsafe_allow_html=True)
