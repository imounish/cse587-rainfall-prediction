# enconding for wind gust direction
windGustDir_encoded = {
    "w": 0,
    "wnw": 1,
    "wsw": 2,
    "ne": 3,
    "nnw": 4,
    "n": 5,
    "nne": 6,
    "sw": 7,
    "ene": 8,
    "sse": 9,
    "s": 10,
    "nw": 11,
    "se": 12,
    "ese": 13,
    "e": 14,
    "ssw": 15,
}

# encoding for wind direction at 9 am
windDir9am_encoded = {
    "w": 0,
    "nnw": 1,
    "se": 2,
    "ene": 3,
    "sw": 4,
    "sse": 5,
    "s": 6,
    "ne": 7,
    "n": 8,
    "ssw": 9,
    "wsw": 10,
    "ese": 11,
    "e": 12,
    "nw": 13,
    "wnw": 14,
    "nne": 15,
}

# encoding for wind direction at 3 pm
windDir3pm_encoded = {
    "wnw": 0,
    "wsw": 1,
    "e": 2,
    "nw": 3,
    "w": 4,
    "sse": 5,
    "ese": 6,
    "ene": 7,
    "nnw": 8,
    "ssw": 9,
    "sw": 10,
    "se": 11,
    "n": 12,
    "s": 13,
    "nne": 14,
    "ne": 15,
}

# encoding for rain today
rainToday_encoded = {"no": 0, "yes": 1}

# define the min and max values for each feature
feature_ranges = {
    "MinTemp": (-8.5, 33.9),
    "MaxTemp": (-4.8, 48.1),
    "Rainfall": (0.0, 371.0),
    "Evaporation": (0.0, 145.0),
    "Sunshine": (0.0, 14.5),
    "WindGustSpeed": (6.0, 135.0),
    # "WindSpeed9am": (0.0, 130.0),
    "WindSpeed9am": (0.0, 135.0),
    # "WindSpeed3pm": (0.0, 87.0),
    "WindSpeed3pm": (0.0, 135.0),
    "Humidity9am": (0.0, 100.0),
    "Humidity3pm": (0.0, 100.0),
    # "Pressure9am": (980.5, 1041.0),
    "Pressure9am": (977.0, 1041.0),
    # "Pressure3pm": (977.1, 1039.6),
    "Pressure3pm": (977.0, 1041.0),
    "Cloud9am": (0.0, 9.0),
    "Cloud3pm": (0.0, 9.0),
    # "Temp9am": (-7.2, 40.2),
    "Temp9am": (-5.5, 46.7),
    # "Temp3pm": (-5.4, 46.7),
    "Temp3pm": (-5.4, 46.7),
}
