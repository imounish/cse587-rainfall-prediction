from fastapi import FastAPI
import joblib
import numpy as np
import pandas as pd
import logging

app = FastAPI()

logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

model_path = "model/knn_model_no_location.sav"

# load model with joblib
loaded_model = joblib.load(model_path)

# Define the encoded values
windGustDir_encoded = {'w': 0, 'wnw': 1, 'wsw': 2, 'ne': 3, 'nnw': 4, 'n': 5, 'nne': 6, 'sw': 7, 'ene': 8, 'sse': 9, 's': 10, 'nw': 11, 'se': 12, 'ese': 13, 'e': 14, 'ssw': 15}
windDir9am_encoded = {'w': 0, 'nnw': 1, 'se': 2, 'ene': 3, 'sw': 4, 'sse': 5, 's': 6, 'ne': 7, 'n': 8, 'ssw': 9, 'wsw': 10, 'ese': 11, 'e': 12, 'nw': 13, 'wnw': 14, 'nne': 15}
windDir3pm_encoded = {'wnw': 0, 'wsw': 1, 'e': 2, 'nw': 3, 'w': 4, 'sse': 5, 'ese': 6, 'ene': 7, 'nnw': 8, 'ssw': 9, 'sw': 10, 'se': 11, 'n': 12, 's': 13, 'nne': 14, 'ne': 15}
rainToday_encoded = {'no': 0, 'yes': 1}

# Define the min and max values for each feature
feature_ranges = {
    'MinTemp': (-8.5, 33.9),
    'MaxTemp': (-4.8, 48.1),
    'Rainfall': (0.0, 371.0),
    'Evaporation': (0.0, 145.0),
    'Sunshine': (0.0, 14.5),
    'WindGustSpeed': (6.0, 135.0),
    'WindSpeed9am': (0.0, 130.0),
    'WindSpeed3pm': (0.0, 87.0),
    'Humidity9am': (0.0, 100.0),
    'Humidity3pm': (0.0, 100.0),
    'Pressure9am': (980.5, 1041.0),
    'Pressure3pm': (977.1, 1039.6),
    'Cloud9am': (0.0, 9.0),
    'Cloud3pm': (0.0, 9.0),
    'Temp9am': (-7.2, 40.2),
    'Temp3pm': (-5.4, 46.7)
}

# Function to preprocess the data
def preprocess_data(data):
    # Replace the categorical values with the corresponding encoded values
    data['WindGustDir'] = data['WindGustDir'].replace(windGustDir_encoded)
    data['WindDir9am'] = data['WindDir9am'].replace(windDir9am_encoded)
    data['WindDir3pm'] = data['WindDir3pm'].replace(windDir3pm_encoded)
    data['RainToday'] = data['RainToday'].replace(rainToday_encoded)

    # Normalize the numerical features
    for col, (min_val, max_val) in feature_ranges.items():
        data[col] = (data[col].astype(float) - min_val) / (max_val - min_val)

    return data



@app.get("/")
def root():
    logger.debug("Root endpoint accessed")
    logger.info("Testing Info")
    logger.warn("Testing Warning")
    logger.error("Testing Error")
    return {"message": "Welcome to the ML Model API"}


@app.post("/predict/")
def predict(data: dict):
    features = pd.DataFrame.from_dict(data["features"])
    # Preprocess the data
    features = preprocess_data(features)
    # Log the preprocessed features
    logging.info(features)
    for f in features:
        # logging.info(f)
        logging.info(features[f])

    prediction = loaded_model.predict(features)
    
    return {"class": prediction[0].item()}
