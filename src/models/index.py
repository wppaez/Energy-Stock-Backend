from models.expo_2 import predict_expo_2

def predict(model_name, samples):
    if model_name == "Exponencial Doble":
        result = predict_expo_2(samples)
    else: 
        result = []
    return result