import streamlit as st

# Function to classify condition
def classify_condition(age, peak_flow, smoking_status, persistent_cough, family_history):
    """
    Classify the condition based on input features.
    """
    # Define thresholds (these are illustrative; adjust based on clinical data)
    normal_peak_flow_min = 400
    normal_peak_flow_max = 700
    copd_peak_flow_threshold = 300  # Below this value suggests COPD
    asthma_peak_flow_variability = 100  # Variability suggesting asthma

    # Classification logic
    if (normal_peak_flow_min <= peak_flow <= normal_peak_flow_max and
        smoking_status == "Never" and
        persistent_cough == "No" and
        family_history == "No"):
        return "Healthy", "green"
    elif (age < 40 and
          peak_flow < normal_peak_flow_min and
          (smoking_status == "Never" or smoking_status == "Former") and
          persistent_cough == "Yes" and
          family_history == "Yes"):
        return "Asthma", "blue"
    else:
        return "COPD", "red"

# Streamlit UI
st.set_page_config(layout="wide")
st.title("🫁 COPD & Asthma Prediction")

# Sidebar for patient input
st.sidebar.header("📝 Patient Information")
age = st.sidebar.slider("Age", 10, 90, 35)
peak_flow = st.sidebar.slider("Peak Flow (L/min)", 100, 700, 479)
smoking_status = st.sidebar.selectbox("Smoking Status", ["Never", "Former", "Current"])
persistent_cough = st.sidebar.selectbox("Persistent Cough", ["No", "Yes"])
family_history = st.sidebar.selectbox("Family History of Asthma", ["No", "Yes"])

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
