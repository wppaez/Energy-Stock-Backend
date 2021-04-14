import datetime
from flask import Flask, request
from datetime import datetime as dt
from models.index import predict

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def do_prediction():
    model = request.args.get('model')
    startQuery = request.args.get('start')
    endQuery = request.args.get('end')
    if model is None or startQuery is None or endQuery is None:
        return {
            "success": False,
            "message": 'One or more query params are missing, the expected query params are: "model", "start", "end"'
        }

    n_samples = getDeltaOfDates(request)
    execution = predict(model, n_samples)
    dates = getDateList(request, n_samples)
    zipped = zip(dates, execution['prediction'])
    predictionWithDates = [{"date": value[0], "value": value[1]} for value in zipped]        
    result = {
        "success": True,
        "range": {
            "start": predictionWithDates[0]['date'],
            "end": predictionWithDates[-1]['date']
        },
        "stats": execution['stats'],
        "prediction": predictionWithDates,
    }
    return result

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
    app.run(debug=True)