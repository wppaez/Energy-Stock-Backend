import os
import numpy as np
from rpy2 import robjects
from .execute_r import run_file

def predict(variable, model_name, samples):
    # models = ['ARIMA', 'Exponencial Doble', 'GARCH', 'TAR', 'Gradient Boosting', 'Red Neuronal']
    models = ['ARIMA', 'Exponencial Doble', 'GARCH', 'Gradient Boosting', 'Red Neuronal', 'SVM']
    if model_name in models: 
        result = run_file(variable, model_name, samples)
    else:
        result = {
            "prediction": [0, 0],
            "stats": {
                "sse": 0.00,
                "mse": 0.00,
                "mape": 0.00,
            }
        }
    return result

def test():
    current_path = os.path.dirname(__file__)
    source = os.path.join(current_path, f'../../models/test.R')
    
    # set source file for rpy2.
    robjects.r.source(source)

    # load var from R script.
    r_output = robjects.globalenv["output"]
    as_list = np.array(r_output).tolist()
    return as_list