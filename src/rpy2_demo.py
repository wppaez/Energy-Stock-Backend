import os
from rpy2 import robjects

def map_model_to_file(model):
    if model == "Exponencial Doble":
        current_path = os.path.dirname(__file__)
        model = os.path.join(current_path, f'../models/expo_2.predict.R')
        return model

def map_model_to_dataset(model):
    if model == "Exponencial Doble":
        return "downloads/formatted_Precio de Bolsa Nacional-001.csv"
        
def predict_expo_2(model, samples):
    # set source file for rpy2.
    robjects.globalenv["input_file"] = map_model_to_dataset(model)
    robjects.globalenv["n_samples"] = samples
    source = map_model_to_file(model)
    print('Source: ', source)
    robjects.r.source(source)

    # load var from R script.
    r_output = robjects.globalenv["output"]
    
    # convert R list to Python list.
    mapped = [v for k, v in r_output.items()]
    prediction = mapped[0]
    return prediction

if __name__ == '__main__':
    predict_expo_2("Exponencial Doble", 31)