"""
driver_profile_api.utils.ml_model_utils
-------

This module provides utilities to deal with ml model
"""

# packages
import onnxruntime as rt
import numpy as np

def predict_profile(path_name, data):
    """
    Predict trips profile

    Args:
        path_name (str): Model path with name
        data (pandas.DataFrame): Trips to predict

    Returns:
        numpy.ndarray: Prediction array with classes
    """
    sess = rt.InferenceSession(path_name + '.onnx')
    input_name = sess.get_inputs()[0].name
    label_name = sess.get_outputs()[0].name
    pred_onx = sess.run([label_name], {input_name: data.to_numpy()})[0]
    return pred_onx