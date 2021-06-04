import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import pickle
import os
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "Jkaa1SmegW7iyLQ5HoAumvAal-Z3jnradP9j1b4iTNbV"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


app = Flask(__name__)
model = pickle.load(open('loan.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('LoanStatus.html')


@app.route('/predict', methods=['POST'])
def predict():
    input_features = [float(x) for x in request.form.values()]
    features_value = [np.array(input_features)]

    features_name = ['Current Loan Amount', 'Term', 'Credit Score', 'Annual Income',
                     'Years in current job', 'Home Ownership', 'Years of Credit History',
                     'Number of Credit Problems', 'Bankruptcies', 'Tax Liens',
                     'Credit Problems', 'Credit Age']
    payload_scoring = {"input_data": [{"fields": [features_name], "values": [input_features]}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/d06ceba3-f576-43a7-8e23-a1d7935dab80/predictions?version=2021-06-04', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    print(predictions)
    pred = predictions['prediction'][0]['values'][0][0]
    if(pred==0):
        output = "he will not get exited"
        print("he will not get exited")
    else:
        output="he gets exited"
        print("he gets exited")
   return render_template('index.html',prediction_text= output)
    
    
 
    
  return render_template('ChargedOff.html')


if __name__ == '__main__':
    app.run(debug=False)
   
