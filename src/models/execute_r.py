import os
import numpy as np
from rpy2 import robjects
import rpy2.robjects.numpy2ri as rpyn


def map_model_to_file(variable, model_name):
    prefix = 'bolsa' if variable == 'Bolsa de Energía' else 'precio'
    current_path = os.path.dirname(__file__)
    if model_name == "ARIMA":
        model_path = os.path.join(current_path, f'../../models/{prefix}.arima.predict.R')
    elif model_name == "Exponencial Doble":
        model_path = os.path.join(current_path, f'../../models/{prefix}.expo.predict.R')
    elif model_name == "GARCH":
        model_path = os.path.join(current_path, f'../../models/{prefix}.garch.predict.R')
    elif model_name == "TAR":
        model_path = os.path.join(current_path, f'../../models/{prefix}.tar.predict.R')
    elif model_name == "SVM":
        model_path = os.path.join(current_path, f'../../models/{prefix}.svm.predict.R')
    elif model_name == "Red Neuronal":
        model_path = os.path.join(current_path, f'../../models/{prefix}.nn.predict.R')
    return model_path

def map_model_to_dataset(variable):
    if(variable == 'Bolsa de Energía'):
            return "downloads/formatted_Precio de Bolsa Nacional.csv"
    else:  
        return [
            "downloads/sized_formatted_Precio de Escasez de Activacion.csv", 
            "downloads/sized_formatted_Precio de Oferta del Despacho.csv"
        ]
          
def run_file(variable, model_name, samples):
    if(variable == 'Bolsa de Energía'):
        robjects.globalenv["input_file"] = map_model_to_dataset(variable)
    else:
        files = map_model_to_dataset(variable)
        robjects.globalenv["escasez_file"] = files[0]
        robjects.globalenv["despacho_file"] = files[1]

    robjects.globalenv["n_samples"] = samples

    source = map_model_to_file(variable, model_name)

    print(f'Forecasting {samples} samples of {variable} with {model_name} model ')
    print(f'Source: {source}')

    # set source file for rpy2.
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
    