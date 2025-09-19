from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd
import time
import requests
import os
load_model = pickle.load(open("ml-deptest.sav", 'rb'))




app = Flask(__name__)

@app.route("/fake")
def fake():
    res = os.system("ls")
    return res

@app.route("/temp")
def team():
    while True:
        time.sleep(5)
        requests.get("https://depressiontest.onrender.com/fake")
    return "temp"



@app.route("/depression", methods=["POST"])
def depression():
    age = float(request.form.get("age"))
    academic_pressure = float(request.form.get("academic_pressure"))
    study_satisfaction = float(request.form.get("study_satisfaction"))
    work_study = float(request.form.get("work_study"))
    financial = float(request.form.get("financial"))

    genderencode = request.form.get("genderencode")
    family_histroy = request.form.get("family_histroy")
    suicidalencoded = request.form.get("suicidalencoded")
    sleep = request.form.get("sleep")
    dietary = request.form.get("dietary")

    #-----------------------gender----------------------

    if genderencode == "Male":
        genderencode = 1
    else:
        genderencode = 0

    # -----------------------dite----------------------

    if dietary == "Healthy":
        dietary = 0
    
    elif dietary == "Moderate":
        dietary = 1
    
    else:  # for unhealthy
        dietary = 3

# --------------------------sleep---------------------

    if sleep == "5-6 hours":
        sleep = 0

    elif sleep == "7-8 hours":
        sleep = 1
    
    elif sleep == "Less than 5 hours":
        sleep = 2

    else:
        sleep = 3
    
    # --------------------suisidal--------------------
        
    if suicidalencoded == "Yes":
        suicidalencoded = 1
    else:
        suicidalencoded = 0



    
# -----------------------------------------for city----------------------------------------------------------------------------------

    if family_histroy == "Yes":
        family_histroy = 1
    else:
        family_histroy = 0
    

    input_qu = np.array([[age,academic_pressure,study_satisfaction,work_study,financial,
                          float(genderencode),float(suicidalencoded),float(sleep),float(dietary),float(family_histroy)]])

    result = str(load_model.predict(input_qu)[0])

    
    return jsonify({'prediction': str(result)})





if __name__ == "__main__":
    app.run(debug="true")
