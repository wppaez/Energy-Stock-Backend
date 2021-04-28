import requests

def requestPlumber(variable, model, samples):
    url = 'http://159.65.170.235/api/forecast'
    query_params = {
        "variable": variable,
        "model": model,
        "samples": samples,
    }

    response = requests.get(url, params=query_params)
    json = response.json()
    stats = json['stats']
    return {
        "forecast": json['forecast'],
        "stats": {
            "mape": stats["MAPE"][0],
            "mse": stats["MSE"][0],
            "sse": stats["SSE"][0],
        }
    }
    
    #print(json['forecast'])
    #print(json['stats'])

if __name__ == "__main__":
    requestPlumber("Precio Unitario", "ARIMA", 30)