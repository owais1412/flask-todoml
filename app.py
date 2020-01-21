from flask import Flask, jsonify, json, request
from flask_cors import CORS, cross_origin
import sklearn
from sklearn import preprocessing
import pandas as pd
import numpy as np
import pickle
import random
import math
import os


# DIR = "C:\\Users\\Owais\\.conda\\envs\\TODO_ML\\server"
# DIR = r"C:\Users\Owais\Desktop\Programming\TODO_ML\server"
# DIR = os.getcwd()
DIR = os.path.realpath(__file__).replace("\\app.py", "")

app = Flask(__name__)
CORS(app)


cls1 = ["Food", "Vegetables", "Grocery", "Buying"]
n = []
for i in cls1:
    x = i + " list"
    y = i + "list"
    n.append(x)
    n.append(y)
cls1.extend(n)
with open(DIR + "\cls1.txt", "w") as f:
    for i in cls1:
        f.write(i+",")


@app.route("/")
def home():
    return "Hii Owais"


@app.route("/predict", methods=["GET", "POST"])
def main():
    with open(DIR+r"\todo_ml.sav", 'rb') as f:
        model = pickle.load(f)
    data = pd.read_csv(DIR+r"\dataset.csv")
    data.drop([" pork"], axis=1, inplace=True)
    data.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)
    # print(data.columns)
    #
    le = preprocessing.LabelEncoder()
    sandwich = le.fit_transform(data[" sandwich bags"])
    lunch_meat = le.fit_transform(data[" lunch meat"])
    all_purpose = le.fit_transform(data[" all- purpose"])
    flour = le.fit_transform(data[" flour"])
    soda = le.fit_transform(data[" soda"])
    butter = le.fit_transform(data[" butter"])
    vegetables = le.fit_transform(data[" vegetables"])
    beef = le.fit_transform(data[" beef"])
    aluminum_foil = le.fit_transform(data[" aluminum foil"])
    all_purpose1 = le.fit_transform(data[" all- purpose.1"])
    dinner_rolls = le.fit_transform(data[" dinner rolls"])
    shampoo = le.fit_transform(data[" shampoo"])
    all_purpose2 = le.fit_transform(data[" all- purpose.2"])

    predict = " all- purpose"

    X = list(zip(sandwich, lunch_meat, flour, soda, butter, vegetables, beef, aluminum_foil, all_purpose1, all_purpose2,
                 dinner_rolls, shampoo))

    # get user input
    payload = request.get_json(force=True)
    key = payload["data"]
    # predict
    y_kmeans = model.predict(X)
    y_kmeans = list(le.inverse_transform(y_kmeans))
    data = []
    for _ in range(5):
        i = math.floor(random.randint(0,1000))
        data.append(y_kmeans[i])

    # send the response
    to_send = {0: "No matching list found"}
    for i in cls1:
        if key in i or key == i:
            to_send = data
    response = app.response_class(
        response=json.dumps(to_send),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/add_suggestions", methods=["GET", "POST"])
def add_suggestions():
    data = request.get_json(force=True)
    to_send = {"0": "No matching list found", "status": "0"}
    l = []
    with open(DIR + "\cls1.txt", "r") as f:
        l.append(f.read())

    if data["status"] == "1":
        if data["data"] not in l[0]:
            cls1.append(data["data"])
            to_send["0"] = "Data added successfully"
            to_send["status"] = "1"
        else:
            to_send["0"] = "Data already present"
            to_send["status"] = "1"
    elif data["status"] == "0":
        to_send["0"] = "Nothing to add"

    with open(DIR + "\cls1.txt", "w") as f:
        for i in cls1:
            f.write(i+",")
    response = app.response_class(
        response=json.dumps(to_send),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/get_list", methods=["GET", "POST"])
def send_list():
    to_send = []
    with open(DIR + "\cls1.txt", "r") as f:
        to_send.append(f.read())
    response = app.response_class(
        response=json.dumps(to_send),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == "__main__":
    app.run()