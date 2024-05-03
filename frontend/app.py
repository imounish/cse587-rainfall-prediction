import streamlit as st
import requests
import json

wind_directions = (
    "West",
    "North & North West",
    "South East",
    "East & North East",
    "South West",
    "South & South East",
    "South",
    "North East",
    "North",
    "South & South West",
    "West & South West",
    "East & South East",
    "East",
    "North West",
    "West & North West",
    "North & North East",
)

wind_directions_encoding = {
    "West": "w",
    "North & North West": "nnw",
    "South East": "se",
    "East & North East": "ene",
    "South West": "sw",
    "South & South East": "sse",
    "South": "s",
    "North East": "ne",
    "North": "n",
    "South & South West": "ssw",
    "West & South West": "wsw",
    "East & South East": "ese",
    "East": "e",
    "North West": "nw",
    "West & North West": "wnw",
    "North & North East": "nne",
}


def main():
    st.title("Rainfall Prediction in Australia")

    temp_col1, temp_col2 = st.columns(2)

    with temp_col1:
        minTemp = st.number_input(
            "Minimum Temperature", min_value=-8.5, max_value=33.9, value=9.7
        )

    with temp_col2:
        maxTemp = st.number_input(
            "Maximum Temperature", min_value=-4.8, max_value=48.2, value=31.9
        )

    rainfall = st.number_input("Rainfall", min_value=0.0, max_value=371.0, value=0.0)

    evaporation = st.number_input(
        "Evaporation", min_value=0.0, max_value=145.0, value=20.0
    )

    sunshine = st.number_input("Sunshine", min_value=0.0, max_value=14.5, value=10.0)

    windGust_col1, windGust_col2 = st.columns(2)

    with windGust_col1:
        windGustDir = st.selectbox(
            "Direction of Wind Gusts",
            wind_directions,
            index=1,
            placeholder="Choose a direction",
        )

    with windGust_col2:
        windGustSpeed = st.number_input(
            "Speed of Wind Gusts", min_value=6.0, max_value=135.0, value=89.0
        )

    wind9am_col1, wind9am_col2 = st.columns(2)

    with wind9am_col1:
        windDir9am = st.selectbox(
            "Direction of Wind at 9 AM",
            wind_directions,
            index=2,
            placeholder="Choose a direction",
        )

    with wind9am_col2:
        windSpeed9am = st.number_input(
            "Speed of Wind at 9 AM", min_value=0.0, max_value=135.0, value=7.0
        )

    wind3pm_col1, wind3pm_col2 = st.columns(2)

    with wind3pm_col1:
        windDir3pm = st.selectbox(
            "Direction of Wind at 3 PM",
            wind_directions,
            index=13,
            placeholder="Choose a direction",
        )

    with wind3pm_col2:
        windSpeed3pm = st.number_input(
            "Speed of Wind at 3 PM", min_value=0.0, max_value=135.0, value=28.0
        )

    if st.button("Predict"):
        input_data = {
            "features": {
                "MinTemp": [str(minTemp)],
                "MaxTemp": [str(maxTemp)],
                "Rainfall": [str(rainfall)],
                "Evaporation": [str(evaporation)],
                "Sunshine": [str(sunshine)],
                "WindGustDir": [wind_directions_encoding[windGustDir]],
                "WindGustSpeed": [str(windGustSpeed)],
                "WindDir9am": [wind_directions_encoding[windDir9am]],
                "WindDir3pm": [wind_directions_encoding[windDir3pm]],
                "WindSpeed9am": [str(windSpeed9am)],
                "WindSpeed3pm": [str(windSpeed3pm)],
                "Humidity9am": ["42"],
                "Humidity3pm": ["9"],
                "Pressure9am": ["1008.9"],
                "Pressure3pm": ["1003.6"],
                "Cloud9am": ["3"],
                "Cloud3pm": ["4"],
                "Temp9am": ["18.3"],
                "Temp3pm": ["30.2"],
                "RainToday": ["0"],
            }
        }

        result = requests.post(
            url=f"{st.secrets.backend.local.url}/{st.secrets.predict_path}",
            data=json.dumps(input_data),
        )
        rainfall = result.json()

        st.success(
            f"It will rain tomorrow"
            if rainfall["class"] == 1
            else f"It will not rain tomorrow"
        )


if __name__ == "__main__":
    main()
