import UI as st
import pandas as pd
import joblib
from datetime import datetime

# Load model, scaler, and features
model = joblib.load("car_price_model.pkl")
scaler = joblib.load("scaler.pkl")
features = joblib.load("features.pkl")

st.title("Car Price Prediction App 🚗")
st.write("Enter car details below to predict its price:")

# Inputs
current_year = datetime.now().year
year = st.number_input("Year", min_value=2000, max_value=current_year + 3, value=2015)
engine_size = st.number_input(
    "Engine Size (L)", min_value=1.0, max_value=6.0, value=2.0
)
mileage = st.number_input("Mileage", min_value=0, max_value=200000, value=50000)
fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "Electric"])
transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
make = st.selectbox("Make", ["Toyota", "Ford", "Honda", "BMW"])

# Encoding (drop_first=True means reference categories are omitted)
make_bmw = 1 if make == "BMW" else 0
make_ford = 1 if make == "Ford" else 0
make_honda = 1 if make == "Honda" else 0
make_toyota = 1 if make == "Toyota" else 0
fuel_type_electric = 1 if fuel_type == "Electric" else 0
fuel_type_petrol = 1 if fuel_type == "Petrol" else 0
trans_manual = 1 if transmission == "Manual" else 0

# Build input row
X_input = pd.DataFrame(
    [
        [
            year,
            engine_size,
            mileage,
            make_bmw,
            make_ford,
            make_honda,
            make_toyota,
            fuel_type_electric,
            fuel_type_petrol,
            trans_manual,
        ]
    ],
    columns=features,
)

# Scale numeric features
X_input[["Year", "Engine Size", "Mileage"]] = scaler.transform(
    X_input[["Year", "Engine Size", "Mileage"]]
)

# Predict
if st.button("Predict Price"):
    prediction = model.predict(X_input)[0]
    prediction = max(0, prediction)  # clip negatives
    st.success(f"Predicted Car Price: ${prediction:,.2f}")
