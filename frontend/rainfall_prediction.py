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

    col1, col2 = st.columns(2)

    with col1:
        minTemp = st.number_input(
            "Minimum Temperature", min_value=-8.5, max_value=33.9, value=9.7
        )

    with col2:
        maxTemp = st.number_input(
            "Maximum Temperature", min_value=-4.8, max_value=48.2, value=31.9
        )

    rainfall = st.number_input("Rainfall", min_value=0.0, max_value=371.0, value=0.0)

    windGustDir = st.selectbox(
        "Direction of Wind Gusts",
        wind_directions,
        index=1,
        placeholder="Choose a direction",
    )

    windDir9am = st.selectbox(
        "Direction of Wind at 9 AM",
        wind_directions,
        index=2,
        placeholder="Choose a direction",
    )

    windDir3pm = st.selectbox(
        "Direction of Wind at 3 PM",
        wind_directions,
        index=13,
        placeholder="Choose a direction",
    )

    if st.button("Predict"):
        input_data = {
            "features": {
                "MinTemp": [str(minTemp)],
                "MaxTemp": [str(maxTemp)],
                "Rainfall": [str(rainfall)],
                "Evaporation": ["20"],
                "Sunshine": ["20"],
                "WindGustDir": [wind_directions_encoding[windGustDir]],
                "WindGustSpeed": ["89"],
                "WindDir9am": [wind_directions_encoding[windDir9am]],
                "WindDir3pm": [wind_directions_encoding[windDir3pm]],
                "WindSpeed9am": ["7"],
                "WindSpeed3pm": ["28"],
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
        price = requests.post(
            url="http://127.0.0.1:8000/predict", data=json.dumps(input_data)
        )
        rainfall = price.json()
        print(rainfall)
        # p = price["prediction"]
        # st.success(f"The Price of the Car is {p} lacks")
        # price("predict is called.")
        st.success(
            f"It will rain tomorrow"
            if rainfall["class"] == 1
            else f"It will not rain tomorrow"
        )


if __name__ == "__main__":
    main()
