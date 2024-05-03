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
            "Minimum Temperature (°C)",
            min_value=-8.5,
            max_value=33.9,
            value=9.7,
            help="The minimum temperature in degrees celsius",
        )

    with temp_col2:
        maxTemp = st.number_input(
            "Maximum Temperature (°C)",
            min_value=-4.8,
            max_value=48.2,
            value=31.9,
            help="The maximum temperature in degrees celsius",
        )

    rainfall = st.number_input(
        "Rainfall recorded for the day (mm)",
        min_value=0.0,
        max_value=371.0,
        value=0.0,
        help="The amount of rainfall recorded for the day in mm",
    )

    evaporation = st.number_input(
        "Evaporation (Class A pan evaporation (mm) in 24 hours to 9 AM)",
        min_value=0.0,
        max_value=145.0,
        value=20.0,
        help="The so-called Class A pan evaporation (mm) in the 24 hours to 9am",
    )

    sunshine = st.slider(
        "Sunshine (#hours in the day)",
        min_value=0.0,
        max_value=14.5,
        value=10.0,
        step=0.5,
        help="The number of hours of bright sunshine in the day.",
    )

    windGust_col1, windGust_col2 = st.columns(2)

    with windGust_col1:
        windGustDir = st.selectbox(
            "Direction of strongest Wind Gust (in 24 hrs to midnight)",
            wind_directions,
            index=1,
            placeholder="Choose a direction",
            help="The direction of the strongest wind gust in the 24 hours to midnight",
        )

    with windGust_col2:
        windGustSpeed = st.number_input(
            "Speed (km/h) of strongest Wind Gust",
            min_value=6.0,
            max_value=135.0,
            value=89.0,
            help="The speed (km/h) of the strongest wind gust in the 24 hours to midnight",
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
            "Wind Speed (km/h) avg over 10 min prior to 9 AM",
            min_value=0.0,
            max_value=135.0,
            value=7.0,
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
            "Wind Speed (km/h) avg over 10 min prior to 3 PM",
            min_value=0.0,
            max_value=135.0,
            value=28.0,
        )

    humidity9am_col1, humidity3pm_col2 = st.columns(2)

    with humidity9am_col1:
        humidity9am = st.number_input(
            "Humidity (%) at 9 AM", min_value=0.0, max_value=100.0, value=42.0
        )

    with humidity3pm_col2:
        humidity3pm = st.number_input(
            "Humidity (%) at 3 PM", min_value=0.0, max_value=100.0, value=9.0
        )

    pressure9am_col1, pressure3pm_col2 = st.columns(2)

    with pressure9am_col1:
        pressure9am = st.number_input(
            "Atmospheric Presssure (hpa) at 9 AM",
            min_value=977.0,
            max_value=1041.0,
            value=1008.9,
            help="Atmospheric pressure (hpa) reduced to mean sea level at 9 AM",
        )

    with pressure3pm_col2:
        pressure3pm = st.number_input(
            "Atmospheric Pressure at 3 PM",
            min_value=977.0,
            max_value=1041.0,
            value=1003.6,
            help="Atmospheric pressure (hpa) reduced to mean sea level at 3 PM",
        )

    cloud9am_col1, cloud3pm_col2 = st.columns(2)

    with cloud9am_col1:
        cloud9am = st.slider(
            "Clouds at 9 AM",
            min_value=0.0,
            max_value=9.0,
            value=3.0,
            step=1.0,
            help='Fraction of sky obscured by cloud at 9am. This is measured in "oktas", which are a unit of eigths.',
        )

    with cloud3pm_col2:
        cloud3pm = st.slider(
            "Clouds at 3 PM",
            min_value=0.0,
            max_value=9.0,
            value=4.0,
            step=1.0,
            help='Fraction of sky obscured by cloud (in "oktas": eighths) at 3pm.',
        )

    temp9am_col1, temp3pm_col2 = st.columns(2)

    with temp9am_col1:
        temp9am = st.number_input(
            "Temperature at 9 AM (°C)",
            min_value=-5.5,
            max_value=46.7,
            value=18.3,
        )

    with temp3pm_col2:
        temp3pm = st.number_input(
            "Temperature at 3 PM (°C)",
            min_value=-5.5,
            max_value=46.7,
            value=30.2,
        )

    rainToday = st.checkbox(
        "It rained today.",
        help="Check the box if the precipitation (mm) in the 24 hours to 9am exceeds 1mm, otherwise leave it unchecked",
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
                "Humidity9am": [str(humidity9am)],
                "Humidity3pm": [str(humidity3pm)],
                "Pressure9am": [str(pressure9am)],
                "Pressure3pm": [str(pressure3pm)],
                "Cloud9am": [str(cloud9am)],
                "Cloud3pm": [str(cloud3pm)],
                "Temp9am": [str(temp9am)],
                "Temp3pm": [str(temp3pm)],
                "RainToday": ["1" if rainToday else "0"],
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
