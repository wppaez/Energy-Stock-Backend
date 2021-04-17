import os
import numpy as np
from rpy2 import robjects
import rpy2.robjects.numpy2ri as rpyn


def map_model_to_file(model_name):
    if model_name == "ARIMA":
        current_path = os.path.dirname(__file__)
        model_path = os.path.join(current_path, f'../../models/arima.predict.R')
    elif model_name == "Exponencial Doble":
        current_path = os.path.dirname(__file__)
        model_path = os.path.join(current_path, f'../../models/expo_2.predict.R')
    elif model_name == "GARCH":
        current_path = os.path.dirname(__file__)
        model_path = os.path.join(current_path, f'../../models/garch.predict.R')
    return model_path

def map_model_to_dataset(model_name):
    if model_name == "ARIMA":
        return "downloads/formatted_Precio de Bolsa Nacional-001.csv"
    if model_name == "Exponencial Doble":
        return "downloads/formatted_Precio de Bolsa Nacional-001.csv"
    if model_name == "GARCH":
        return "downloads/formatted_Precio de Bolsa Nacional-001.csv"
        
def run_file(model_name, samples):
    # set source file for rpy2.
    robjects.globalenv["input_file"] = map_model_to_dataset(model_name)
    robjects.globalenv["n_samples"] = samples
    source = map_model_to_file(model_name)
    robjects.r.source(source)

    # load var from R script.
    r_output = robjects.globalenv["output"]
    r_SSE = robjects.globalenv["py_SSE"]
    r_MSE = robjects.globalenv["py_MSE"]
    r_MAPE = robjects.globalenv["py_MAPE"]
    
    # generate response casting every variable as lists for dictionary
    execution = {
        "prediction": np.array(r_output).tolist()[0],
        "stats": {
            "sse": np.array(r_SSE).tolist()[0],
            "mse": np.array(r_MSE).tolist()[0],
            "mape": np.array(r_MAPE).tolist()[0],
        }
    }

    return execution
    