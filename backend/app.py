from fastapi import FastAPI
import joblib
import numpy as np
import pandas as pd

app = FastAPI()

model_path = "model/knn_model_no_location.sav"

# load model with joblib
loaded_model = joblib.load(model_path)


@app.get("/")
def root():
    return {"message": "Welcome to the ML Model API"}


@app.post("/predict/")
def predict(data: dict):
    features = pd.DataFrame.from_dict(data["features"])

    prediction = loaded_model.predict(features)

    return {"class": prediction[0].item()}
