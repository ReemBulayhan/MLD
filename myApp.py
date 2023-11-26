

import streamlit as st
import pickle
import pandas as pd
from PIL import Image

# Load the Random Forest model
rf_model = pickle.load(open("rf_model1", "rb"))

# Load the ordinal encoder
enc = pickle.load(open("transformer1", "rb"))

# Function to predict car price
def predict_price(features):
    # Convert features to a DataFrame
    features_df = pd.DataFrame([features], columns=["age", "hp_kW", "km", "Gearing_Type", "make_model"])

    # Apply the ordinal encoder to the categorical features
    features_df[["Gearing_Type", "make_model"]] = enc.transform(features_df[["Gearing_Type", "make_model"]])

    # Make predictions using the Random Forest model
    predicted_price = rf_model.predict(features_df)
    return predicted_price

# Function to set custom page style
def set_page_style():
    st.markdown(
        """
        <style>
            .big-font {
                font-size: 36px !important;
                color: #ff6347 !important;
            }
            .highlight {
                background-color: #f0f8ff;
                padding: 10px;
                border-radius: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Function to display a creative header
def display_header():
    st.title("🚗 Car Price Predictor 🚗")
    st.markdown("### Your journey to affordable luxury begins here!")
    st.image("car_image.jpg", use_column_width=True)

# Main function
def main():
    set_page_style()
    st.set_page_config(
        page_title="Car Price Prediction App",
        page_icon="🚗",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    display_header()

    # Sidebar for user input
    st.sidebar.header("Enter Car Details")
    age = st.sidebar.slider("Car's Age", min_value=1, max_value=20, value=5)
    hp_kW = st.sidebar.slider("Horsepower (kW)", min_value=50, max_value=500, value=100)
    km = st.sidebar.slider("Kilometers driven", min_value=0, max_value=200000, value=50000)

    # Choose Gearing Type and Car Model from a list
    gearing_type_options = ["Automatic", "Manual", "Semi-automatic"]
    selected_gearing_type = st.sidebar.selectbox("Gearing Type", gearing_type_options)

    make_model_options = ["Audi A3", "Audi A1", "Opel Insignia", "Opel Astra", "Opel Corsa", "Renault Clio", "Renault Espace", "Renault Duster", "Audi A2"]
    selected_make_model = st.sidebar.selectbox("Car Model", make_model_options)

    # Input features
    features = {
        "age": age,
        "hp_kW": hp_kW,
        "km": km,
        "Gearing_Type": selected_gearing_type,
        "make_model": selected_make_model
    }

    # Make prediction
    if st.sidebar.button("Predict Price", key="predict_button"):
        predicted_price = predict_price([features["age"], features["hp_kW"], features["km"], features["Gearing_Type"], features["make_model"]])
        st.sidebar.success(f"### Predicted Price: ${predicted_price[0]:,.2f}")

    # Additional creative elements
    st.write("""
        ## Welcome to the Car Price Prediction App!

        Explore the magic of predicting car prices with our state-of-the-art model. Simply enter the details on the sidebar, and let the adventure begin!
        """)

    st.markdown("<div class='highlight'>", unsafe_allow_html=True)
    st.markdown("### Why Choose Our App?")
    st.write("🌟 Creative Design")
    st.write("🚗 Accurate Predictions")
    st.write("🔮 Explore Affordable Luxury")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<p class='big-font'>Ready to embark on your car price prediction journey?</p>", unsafe_allow_html=True)
    st.button("Start Predicting", key="start_button")

if __name__ == "__main__":
    main()
