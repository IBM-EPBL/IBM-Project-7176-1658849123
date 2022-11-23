import numpy as np
import flask
from flask import Flask, render_template, request, jsonify
import pickle
import inputScript
from werkzeug.exceptions import HTTPException
app = Flask(__name__)
model = pickle.load(open('Phishing_Website.pkl','rb'))
@app.route('/predict')
def predict():
    return flask.render_template('final.html')
@app.route('/y_predict', methods = ['POST'])
def y_predict():
    url = request.form['URL']
    checkprediction = inputScript.main(url)
    prediction = model.predict(checkprediction)
    output = prediction[0]
    if(output == 1):
        pred = "You are safe !!  This is a Legitimate Website."
    else:
        pred = "Please be cautious !! The website is harmful. !"
    return render_template('final.html',prediction_text='{}'.format(pred),url=url)
@app.route('/predict_api',methods=['POST','GET'])
def predict_api():
    data = request.get_json()
    prediction = model.y_predict([np.array(list(data.values()))])
    output = prediction[0]
    return jsonify(output)
@app.errorhandler(HTTPException)
def handleError(err):
    return render_template("message.html",title=err.name, message=err.description),err.code
if __name__ == '__main__':
    app.run('0.0.0.0')    