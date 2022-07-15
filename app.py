from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import requests
from joblib import load

app = Flask(__name__)

requests.get('https://sagemaker-brae-data.s3.eu-west-2.amazonaws.com/rfc_model.joblib')
requests.get('https://sagemaker-brae-data.s3.eu-west-2.amazonaws.com/encoder.joblib')
requests.get('https://sagemaker-brae-data.s3.eu-west-2.amazonaws.com/scaler.joblib')

model = load('rfc_model.joblib')
enc = load('encoder.joblib')
scaler = load('scaler.joblib')

cat_feature_cols = ["job", "marital", "education", "default", "housing", "loan", "contact", "day", "month", "poutcome"]
num_feature_cols = ["age", "balance", "pdays",  "campaign", "previous"]

@app.route('/api/predict', methods=['POST'])
def predict():
    data_json = request.json
    df_json = pd.DataFrame(data_json)
    df_json['day'] = df_json['day'].astype(object)
    input_cat_encoded = enc.transform(df_json[cat_feature_cols])
    input_num_scaled = scaler.transform(df_json[num_feature_cols])
    input = np.concatenate((input_cat_encoded.toarray(), input_num_scaled), axis=1)
    pred = model.predict_proba(input)
    return jsonify({"probability": pred[0,1]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=False)