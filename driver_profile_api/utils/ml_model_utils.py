"""
driver_profile_api.utils.ml_model_utils
-------

This module provides utilities to deal with ml model
"""

# packages
import joblib


def predict_trip_profile(path, x_test):
    """
    Predict trips profile

    Args:
        path_name (str): Model path with name
        x_test (pandas.DataFrame): Trips to predict

    Returns:
        numpy.ndarray: Prediction array with classes
    """
    y_pred = None
    with open(path + '.joblib', 'rb') as f:
        model = joblib.load(f)
        y_pred = model.predict(x_test)
    return y_pred
