from models.execute_r import run_file

def predict(variable, model_name, samples):
    # models = ['ARIMA', 'Exponencial Doble', 'GARCH', 'TAR', 'Gradient Boosting', 'Red Neuronal']
    models = ['ARIMA', 'Exponencial Doble', 'GARCH', 'Gradient Boosting', 'Red Neuronal']
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