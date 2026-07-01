import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import svm
import warnings


def show():
    import streamlit as st

    st.title("Voice Assessment")


warnings.filterwarnings("ignore")

# 1. Resolve dataset path relative to this file's location
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "parkinsons.csv")

# 2. Load dataset (Executes only once on module import)
parkinsons_data = pd.read_csv(csv_path)

# 3. Feature Extraction
X = parkinsons_data.drop(columns=["name", "status"], axis=1)
Y = parkinsons_data["status"]

# 4. Train-Test Split (Exactly as in notebook)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)

# 5. Data Standardization
scaler = StandardScaler()
scaler.fit(X_train.values)  # .values prevents sklearn feature name warnings
X_train_scaled = scaler.transform(X_train.values)

# 6. Modeling (Executes only once on module import)
model = svm.SVC(kernel="linear")
model.fit(X_train_scaled, Y_train)


def predict_voice(features):
    """
    Accepts exactly 22 manually extracted acoustic features.
    Returns prediction dictionary.
    """
    # Convert input to numpy array
    input_data_as_numpy_array = np.asarray(features)

    # Reshape the numpy array for single prediction
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)

    # Standardize the data using the pre-fitted scaler
    std_data = scaler.transform(input_data_reshaped)

    # Predict
    prediction = model.predict(std_data)[0]

    # Return formatted result without printing
    if prediction == 0:
        return {"prediction": int(prediction), "label": "Healthy"}
    else:
        return {"prediction": int(prediction), "label": "Parkinson"}
