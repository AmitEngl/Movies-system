import numpy as np
import pandas as pd
import json
import pickle
from flask import Flask, request, jsonify, render_template
import os

PKL_FILE_NAME = 'iris_rfc_pkl'
app = Flask(__name__)
model = pickle.load(open(PKL_FILE_NAME, 'rb'))

@app.route('/test')
def test():
    """
       test
    """

    return render_template('index5.html')

@app.route('/predict_single')
def predict2():
    """
       function for predicting a single row input by client requests as parameters of the URL
       :return: single prediction label [0,1,2]
       """
    values = [np.array([request.args.get(x) for x in request.args])]
    predict_request = model.predict(values)
    return str(predict_request[0])


@app.route('/predict_multiple', methods=["POST"])
def results():
    """
       function for predicting a test dataset input as a body of the HTTP request
       :return: prediction labels array
       """
    data = request.get_json(force=True)
    data = pd.DataFrame(json.loads(data))
    prediction = model.predict(data)
    output = list(map(int, prediction))
    return jsonify(output)


if __name__ == '__main__':
    port = os.environ.get('PORT')
    app.run(host='0.0.0.0', port=int(port), debug=True)