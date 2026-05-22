import streamlit as st
import pandas as pd
import pickle
from datetime import datetime

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Vehicle Price Predictor",
    page_icon="🚗",
    layout="wide"
)

# -------------------------------------------------
# CUSTOM THEME CSS
# -------------------------------------------------
st.markdown("""
<style>

body {
    background-color: #0f172a;
}

/* Main background */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
}

/* Header Gradient */
.header {
    padding: 30px;
    border-radius: 15px;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    text-align: center;
    margin-bottom: 25px;
}

/* Card style */
.card {
    background: #1e293b;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
    margin-bottom: 20px;
}

/* Result Box */
.result-box {
    background: linear-gradient(90deg, #06b6d4, #3b82f6);
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    color: white;
    font-size: 28px;
    font-weight: bold;
}

.stButton>button {
    background: linear-gradient(45deg, #22d3ee, #6366f1);
    color: white;
    font-weight: bold;
    height: 50px;
    border-radius: 10px;
}

label, .stSelectbox, .stNumberInput, .stTextInput {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# LOAD MODEL
# -------------------------------------------------
@st.cache_resource
def load_model():
    with open("gradient_boosting_vehicle_model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown("""
<div class="header">
<h1>🚗 Used Vehicle Price Predictor</h1>
<p>AI Powered Resale Value Estimation</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# INPUT SECTION
# -------------------------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    vehicle_type = st.selectbox(
        "Vehicle Type",
        ["Bike", "Scooter", "Car", "Bus", "Van",
         "Auto_Rickshaw", "Electric_Car", "Electric_Scooter"]
    )

    brand = st.text_input("Brand")

    manufacture_year = st.number_input(
        "Manufacture Year",
        min_value=1990,
        max_value=datetime.now().year,
        value=2020
    )

    km_driven = st.number_input("KM Driven", min_value=0)

    fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "Electric"])
    transmission_type = st.selectbox("Transmission Type", ["Manual", "Automatic"])

with col2:
    owner_count = st.number_input("Owner Count", min_value=1, max_value=5)
    engine_capacity_cc = st.number_input("Engine Capacity (cc)", min_value=0)
    mileage_kmpl = st.number_input("Mileage (kmpl)", min_value=0.0)

    registration_city = st.selectbox(
        "Registration City",
        ["Hyderabad", "Vijayawada", "Visakhapatnam", "Guntur", "Warangal"]
    )

    insurance_status = st.selectbox("Insurance Status", ["Yes", "No"])
    accident_record = st.selectbox("Accident History", ["Yes", "No"])
    color = st.selectbox(
        "Vehicle Color",
        ["White", "Black", "Silver", "Red", "Blue", "Grey"]
    )

vehicle_age = datetime.now().year - manufacture_year
st.info(f"🚘 Vehicle Age: {vehicle_age} years")

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# PREDICTION
# -------------------------------------------------
if st.button("💰 Predict Price", use_container_width=True):

    if brand.strip() == "":
        st.warning("Please enter vehicle brand.")
        st.stop()

    input_data = pd.DataFrame([{
        "vehicle_type": vehicle_type,
        "brand": brand,
        "manufacture_year": manufacture_year,
        "vehicle_age": vehicle_age,
        "km_driven": km_driven,
        "fuel_type": fuel_type,
        "transmission_type": transmission_type,
        "owner_count": owner_count,
        "engine_capacity_cc": engine_capacity_cc,
        "mileage_kmpl": mileage_kmpl,
        "registration_city": registration_city,
        "insurance_status": insurance_status,
        "accident_record": accident_record,
        "color": color
    }])

    prediction = model.predict(input_data)[0]

    st.markdown(f"""
    <div class="result-box">
    Estimated Resale Price <br><br>
    ₹ {int(prediction):,}
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown(
    """
    <br><br>
    <center style="color:#94a3b8">
    AI Vehicle Pricing System © 2026
    </center>
    """,
    unsafe_allow_html=True
)


