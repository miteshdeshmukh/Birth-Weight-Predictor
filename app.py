from flask import Flask,request,jsonify,render_template
import pandas as pd
import pickle
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)
print("USER:", os.getenv("MYSQL_USER"))
print("PASS:", os.getenv("MYSQL_PASSWORD"))
print("DB:", os.getenv("MYSQL_DB"))

app=Flask(__name__)


db = mysql.connector.connect(
    host="127.0.0.1",
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DB")
)


def get_cleaned_data(form_data):
    gestation=float(form_data['gestation'])
    parity=int(form_data['parity'])
    age=float(form_data['age'])
    height=float(form_data['height'])
    weight=float(form_data['weight'])
    smoke=float(form_data['smoke'])
    cleaned_data={
        "gestation":[gestation],
        "parity":[parity],
        "age":[age],
        "height":[height],
        "weight":[weight],
        "smoke":[smoke]
    }
    return cleaned_data



@app.route('/',methods=['GET'])
def home():
    return render_template("index.html")

@app.route('/hello',methods=['GET'])
def hello():
    return "hello world!!"

@app.route('/predict',methods=['POST'])
def get_prediction():
    baby_data_form=request.form
    baby_data_cleaned=get_cleaned_data(baby_data_form)
    baby_df=pd.DataFrame(baby_data_cleaned)
    with open("model1.pkl","rb") as obj:
        model=pickle.load(obj)
    prediction=model.predict(baby_df)
    prediction=round(float(prediction[0]),2)
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO predictions 
        (gestation, parity, age, height, weight, smoke, predicted_weight)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        baby_data_cleaned["gestation"][0],
        baby_data_cleaned["parity"][0],
        baby_data_cleaned["age"][0],
        baby_data_cleaned["height"][0],
        baby_data_cleaned["weight"][0],
        baby_data_cleaned["smoke"][0],
        prediction
    ))

    db.commit()

    response={"prediction":prediction}
    return render_template('index.html',prediction=prediction)


if __name__=='__main__':
    app.run(debug=True)