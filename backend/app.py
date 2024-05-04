from fastapi import FastAPI
import joblib
import pandas as pd
import logging

from utils import (
    windGustDir_encoded,
    windDir9am_encoded,
    windDir3pm_encoded,
    feature_ranges,
    rainToday_encoded,
)

app = FastAPI()

# basic logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    filename="app.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
)
# install logger
logger = logging.getLogger(__name__)

# set the model path
model_path = "model/knn_model_no_location.sav"

# load model with joblib
loaded_model = joblib.load(model_path)


# Function to preprocess the data
def preprocess_data(data):
    # Replace the categorical values with the corresponding encoded values
    data["WindGustDir"] = data["WindGustDir"].replace(windGustDir_encoded)
    data["WindDir9am"] = data["WindDir9am"].replace(windDir9am_encoded)
    data["WindDir3pm"] = data["WindDir3pm"].replace(windDir3pm_encoded)
    data["RainToday"] = data["RainToday"].replace(rainToday_encoded)

    # Normalize the numerical features
    for col, (min_val, max_val) in feature_ranges.items():
        data[col] = (data[col].astype(float) - min_val) / (max_val - min_val)

    return data


@app.get("/")
def root():
    return {"message": "Welcome to the ML Model API"}


@app.post("/predict/")
def predict(data: dict):
    features = pd.DataFrame.from_dict(data["features"])

    # Preprocess the data
    features = preprocess_data(features)

    # for f in features:
    #     logging.info(features[f])

    prediction = loaded_model.predict(features)

    return {"class": prediction[0].item()}
