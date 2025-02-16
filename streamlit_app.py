import streamlit as st

# Page Configuration
st.set_page_config(page_title="COPD & Asthma Prediction", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        .title-container {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        .title-container img {
            width: 40px;
            height: 40px;
        }
        .header-text {
            font-size: 30px;
            font-weight: bold;
        }
        .sub-header {
            text-align: center;
            font-size: 16px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Add "PFA - Digital Transformation" above the title
st.markdown('<p class="sub-header">PFA - Digital Transformation</p>', unsafe_allow_html=True)

# COPD & Asthma Prediction Title with Lung Icon
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown("""
        <div class="title-container">
            <img src="https://cdn-icons-png.flaticon.com/512/3209/3209026.png" alt="Lung Icon">
            <span class="header-text">COPD & Asthma Prediction</span>
        </div>
    """, unsafe_allow_html=True)

# Your existing prediction form or logic goes here...
