from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd

load_model = pickle.load(open("depression_logistic_with_85_new.sav", 'rb'))

status = "off"


app = Flask(__name__)

@app.route("/nodemcu")
def nodemcu():
    return status

@app.route("/webpython")
def webpython():
    status = "on"
    return status


@app.route("/depression", methods=["POST"])
def depression():
    age = float(request.form.get("age"))
    academic_pressure = float(request.form.get("academic_pressure"))
    study_satisfaction = float(request.form.get("study_satisfaction"))
    work_study = float(request.form.get("work_study"))
    financial = float(request.form.get("financial"))

    genderencode = request.form.get("genderencode")
    cityencode = request.form.get("cityencode")
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

    if cityencode == "Yes":
        cityencode = 1
    else:
        cityencode = 0
    
    # df = pd.read_csv("citydata3.csv")
    # df.drop("id",axis=1)
    # capitalized_string = cityencode.capitalize()
    # df_cleaned = df.drop_duplicates(subset=['name'])
    # rows_with_age_25 = df_cleaned.loc[df_cleaned['name'] == capitalized_string]
    # cityencode = rows_with_age_25["code"].to_list()[0]


    
    



    input_qu = np.array([[age,academic_pressure,study_satisfaction,work_study,financial,
                          float(genderencode),float(suicidalencoded),float(sleep),float(dietary),float(cityencode)]])

    result = str(load_model.predict(input_qu)[0])

    # return jsonify({'gender':str(genderencode),
    #                 'city': str(cityencode),
    #                 'suicidal': str(suicidalencoded),
    #                 'sleep': str(sleep),
    #                 'dite': str(dietary)})

    return jsonify({'prediction': str(result)})

    # if result == "1":
    #     return jsonify("You Are At Risk Of Depression Please Seek Help ASAP!!!")
    
    # else:
    #     return jsonify("You Are Currently Not At Risk Of Depression Take Care...")





if __name__ == "__main__":
    app.run(debug="true")
