import streamlit as st
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Initialize encoders and scaler
label_encoders = {
    "Smoking Status": LabelEncoder().fit(["Never", "Former", "Current"]),
    "Persistent Cough": LabelEncoder().fit(["No", "Yes"]),
    "Family History": LabelEncoder().fit(["No", "Yes"]),
    "Condition": LabelEncoder().fit(["Healthy", "Asthma", "COPD", "ACOS"])
}
scaler = StandardScaler()

# Placeholder model (replace with a trained model)
model = RandomForestClassifier()

# Set page configuration
st.set_page_config(page_title="COPD-Asthma Prediction App", page_icon="🫁", layout="wide")

# Title and header
st.markdown("<h1 style='text-align: center;'>PFA - Digital Transformation</h1>", unsafe_allow_html=True)
st.title("🫁 COPD & Asthma Prediction App")

# Sidebar for user input
st.sidebar.header("📝 Enter Patient Information")
age = st.sidebar.slider("Age", 10, 90, 40)
symptom_onset_age = st.sidebar.slider("Age at Symptom Onset", 0, 90, 30)
peak_flow = st.sidebar.slider("Peak Flow (L/min)", 100, 700, 350)
smoking_status = st.sidebar.selectbox("Smoking Status", ["Never", "Former", "Current"])
persistent_cough = st.sidebar.selectbox("Persistent Cough", ["No", "Yes"])
family_history = st.sidebar.selectbox("Family History of Asthma", ["No", "Yes"])
symptom_variability = st.sidebar.selectbox("Symptom Variability", ["No", "Yes"])
bronchodilator_response = st.sidebar.slider("Bronchodilator Response (%)", 0, 100, 10)

# Encode categorical variables
smoking_status_encoded = label_encoders["Smoking Status"].transform([smoking_status])[0]
persistent_cough_encoded = label_encoders["Persistent Cough"].transform([persistent_cough])[0]
family_history_encoded = label_encoders["Family History"].transform([family_history])[0]

# Prepare input data
input_data = np.array([[age, symptom_onset_age, peak_flow, smoking_status_encoded,
                        persistent_cough_encoded, family_history_encoded,
                        symptom_variability == "Yes", bronchodilator_response]])

# Scale the input data
input_data_scaled = scaler.transform(input_data)

# Make a prediction
prediction = model.predict(input_data_scaled)
predicted_condition = label_encoders["Condition"].inverse_transform(prediction)[0]

# Define color mapping for conditions
condition_colors = {
    "Healthy": "green",
    "Asthma": "blue",
    "COPD": "red",
    "ACOS": "orange"
}

# Display prediction
st.subheader("📌 Prediction Result")
st.markdown(f'<div style="background-color:{condition_colors[predicted_condition]};'
            f'padding:15px;border-radius:10px;text-align:center;color:white;">'
            f'<strong>Predicted Condition: {predicted_condition}</strong></div>',
            unsafe_allow_html=True)

# Additional model details
with st.expander("🔎 Model Details"):
    st.write("🔹 **Model Raw Prediction:**", prediction[0])
    st.write("🔹 **Prediction Probabilities:**")
    st.table(model.predict_proba(input_data_scaled))
    st.write("🔹 **Condition Class Labels:**")
    st.table(label_encoders["Condition"].classes_)

# Footer
st.markdown("<hr><p style='text-align: center;'>Created by <b>Ehab Essam</b></p>", unsafe_allow_html=True)
