import streamlit as st
import requests
import json
import pandas as pd

from definitions import (
    wind_directions,
    wind_directions_encoding,
    visualization_feature_names,
    visualization_selection_encoding,
)

# import the visualisation dataset for frontend
weather_data = pd.read_csv("weatherAUS_frontend_viz.csv")


def main():
    st.title("Rainfall Prediction in Australia")

    st.caption(
        "Our product tells you with an accuracy of :red[80%] whether it will :blue-background[**rain tomorrow**] :umbrella: or :blue-background[**not**] :sunny:."
    )

    st.markdown(
        """Use the :blue-background[**Prediction**] tab to manually enter the values for each feature and our :red[**KNN Model**] would make the prediction if it rains tomorrow. 
        Use the :blue-background[**Visualization**] tab to see the correlations between various features in the dataset we used."""
    )

    # create tabs for prediction and visualization
    prediction_tab, visualization_tab = st.tabs(["Prediction", "Visualization"])

    with prediction_tab:
        with st.container():
            # input the values for all features
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

            # if user has clicked predict button
            if st.button("Predict", use_container_width=1):
                # make a dict of user input data
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

                # make a post request to backend API
                result = requests.post(
                    url=f"{st.secrets.backend.local.url}/{st.secrets.predict_path}",
                    data=json.dumps(input_data),
                )
                # get rainfall prediction
                rainfall = result.json()

                # show the output based on result class
                st.success(
                    f"It will rain tomorrow"
                    if rainfall["class"] == 1
                    else f"It will not rain tomorrow"
                )

    with visualization_tab:
        st.subheader(
            "Distribution of features vs Rain Tomorrow",
            divider="red",
        )

        with st.container():
            # input feature from user for bar graph
            bar_graph_selection = st.selectbox(
                "Select a feature",
                visualization_feature_names,
                index=0,
            )

            if (
                st.button(
                    "Show Bar graph of {} vs Rain Tomorrow".format(bar_graph_selection)
                )
                and bar_graph_selection
            ):
                # show the bar graph between user input feature and rain tomorrow
                st.bar_chart(
                    weather_data,
                    x=visualization_selection_encoding[bar_graph_selection],
                    y="RainTomorrow",
                )

        st.subheader(
            "Scatter Plot between two features",
            divider="red",
        )

        with st.container():
            # input feature 1 from user for scatter plot
            scatter_plot_selection_1 = st.selectbox(
                "Select a feature 1",
                visualization_feature_names,
                index=0,
            )

            # input feature 2 from user for scatter plot
            scatter_plot_selection_2 = st.selectbox(
                "Select a feature 2",
                visualization_feature_names,
                index=1,
            )

            if (
                st.button(
                    "Show scatter plot of {} vs {}".format(
                        scatter_plot_selection_1, scatter_plot_selection_2
                    )
                )
                and scatter_plot_selection_1
                and scatter_plot_selection_2
            ):
                # show the scatter plot between user input feature 1 and feature 2
                st.scatter_chart(
                    weather_data,
                    x=visualization_selection_encoding[scatter_plot_selection_1],
                    y=visualization_selection_encoding[scatter_plot_selection_2],
                )


if __name__ == "__main__":
    main()
