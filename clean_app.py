import streamlit as st
import pandas as pd
import joblib
import pickle
import requests

# Load model
@st.cache_data
def load_model():
    model = joblib.load("diamond_price_model.pkl")
    with open("label_encoders.pkl", "rb") as f:
        encoders = pickle.load(f)
    return model, encoders

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_exchange_rate():
    """Get current USD to INR exchange rate"""
    try:
        # Using a free API for exchange rates
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        if response.status_code == 200:
            data = response.json()
            return data['rates']['INR']
    except:
        pass
    # Fallback rate if API fails
    return 83.0

model, encoders = load_model()

# App
st.title("💎 Diamond Price Predictor")

# Currency selection
st.subheader("Currency Options")
currency = st.selectbox("Select Currency", ["USD ($)", "INR (₹)"], index=1)

# Input form
col1, col2 = st.columns(2)

with col1:
    st.subheader("Physical Properties")
    carat = st.number_input("Carat Weight", min_value=0.1, max_value=5.0, value=1.0, step=0.01)
    depth = st.number_input("Depth (%)", min_value=50.0, max_value=80.0, value=62.0, step=0.1)
    table = st.number_input("Table (%)", min_value=40.0, max_value=80.0, value=57.0, step=0.1)

with col2:
    st.subheader("Dimensions (mm)")
    x = st.number_input("Length", min_value=2.0, max_value=15.0, value=5.0, step=0.1)
    y = st.number_input("Width", min_value=2.0, max_value=15.0, value=5.0, step=0.1)
    z = st.number_input("Height", min_value=1.0, max_value=10.0, value=3.0, step=0.1)

st.subheader("Quality Grades")
col3, col4, col5 = st.columns(3)

with col3:
    cut = st.selectbox("Cut", ["Fair", "Good", "Very Good", "Premium", "Ideal"])
with col4:
    color = st.selectbox("Color", ["D", "E", "F", "G", "H", "I", "J"])
with col5:
    clarity = st.selectbox("Clarity", ["IF", "VVS1", "VVS2", "VS1", "VS2", "SI1", "SI2", "I1"])

# Predict
if st.button(" Predict Price", type="primary", use_container_width=True):
    # Encode
    cut_encoded = encoders['quality'][cut]
    color_encoded = encoders['color'][color]
    clarity_encoded = encoders['clarity'][clarity]
    
    # Predict
    input_data = pd.DataFrame({
        "carat": [carat], "depth": [depth], "table": [table],
        "x": [x], "y": [y], "z": [z],
        "quality_encoded": [cut_encoded], "color_encoded": [color_encoded], "clarity_encoded": [clarity_encoded]
    })
    
    price_usd = model.predict(input_data)[0]
    
    # Convert to selected currency
    if currency == "INR (₹)":
        exchange_rate = get_exchange_rate()
        price_inr = price_usd * exchange_rate
        st.success(f" **Predicted Price: ₹{price_inr:,.2f}**")
        st.caption(f"*Based on current exchange rate: 1 USD = ₹{exchange_rate:.2f}*")
    else:
        st.success(f" **Predicted Price: ${price_usd:,.2f}**")
    
    # Summary
    st.info(f"**{carat}ct {cut} {color} {clarity} diamond** | Dimensions: {x}×{y}×{z}mm")
