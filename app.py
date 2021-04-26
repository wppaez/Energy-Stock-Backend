from flask import Flask, request
from flask_cors import CORS, cross_origin

import math
import datetime
from datetime import datetime as dt

from src.models.index import predict
from src.utilities.xm_api import run

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/predict', methods=['POST'])
@cross_origin()
def do_prediction():
    variable = request.args.get('variable')
    model = request.args.get('model')
    startQuery = request.args.get('start')
    endQuery = request.args.get('end')

    variableList = ['Bolsa de Energía', 'Precio Unitario'] 
    modelList = ['ARIMA', 'Exponencial Doble', 'GARCH', 'TAR', 'Maquina de Vectores', 'Red Neuronal'] 
    
    variableIsValid = variable is not None and variable in variableList
    modelIsValid = model is not None and model in modelList
    startIsValid = startQuery is not None and len(startQuery.split('-')) == 3
    endIsValid = endQuery is not None and len(endQuery.split('-')) == 3
    if not variableIsValid or not modelIsValid or not startIsValid or not endIsValid:
        return {
            "success": False,
            "message": 'One or more query params are missing or doesn\'t has the expected format, the expected query params are: "variable", "model", "start", "end"'
        }

    n_samples = getDeltaOfDates(request)
    execution = predict(variable, model, n_samples)
    dates = getDateList(request, n_samples)
    zipped = zip(dates, execution['prediction'])
    predictionWithDates = [{"date": value[0], "value": value[1]} for value in zipped]        
    power = 1
    max_v = max(execution['prediction'])
    min_v = min(execution['prediction'])
    power = (10 ** (math.floor(math.log10(max_v -min_v))) if max_v -min_v > 0 else 0)
    result = {
        "success": False if power == 0 else True,
        "variable": variable,
        "range": {
            "date": {
                "min": predictionWithDates[0]['date'],
                "max": predictionWithDates[-1]['date']
            },
            "value": {
                "min": min_v,
                "max": max_v
            }
        },
        "delta": power,
        "stats": execution['stats'],
        "prediction": predictionWithDates,
    }
    return result

@app.route('/update/datasets', methods=['PUT'])
@cross_origin()
def update_dataset():
    try:
        run()
        return {
            "success": True,
            "message": 'Updated datasets.'
        }
    except Exception as e:
        logging.critical(e, exc_info=True)
        logger.warn("...")
        raise

        return {
            "success": False,
            "message": 'The system was no able to update the datasets.'
        }

@app.route('/status', methods=['GET'])
@cross_origin()
def get_status():
    return {
        "success": True,
        "status": 'Online'
    }

@app.route("/")
@cross_origin()
def hello():
    return "<h1 style='color:blue'>Energy Stock Back-end</h1>"

def getDeltaOfDates(request):
    startStr = request.args.get('start')
    endStr = request.args.get('end')
    start = dt.strptime(startStr, '%Y-%m-%d')
    end = dt.strptime(endStr, '%Y-%m-%d')
    delta = end - start
    return delta.days

def destructDate(request, key):
    dateStr = request.args.get(key)
    values = [int(value) for value in dateStr.split('-')]
    date = {
        "year": values[0],
        "month": values[1],
        "day": values[2],
    }
    return date

def getDateList(request, n_samples):
    startDict = destructDate(request, 'start')
    start = datetime.date(startDict['year'], startDict['month'], startDict['day'])
    dates = [start + datetime.timedelta(days=value) for value in range(n_samples)]
    isoDates = [curr.strftime("%Y-%m-%dT%H:%M:%SZ") for curr in dates]
    return isoDates

if __name__ == '__main__':
    app.run(host='0.0.0.0')