from flask import Flask,request,jsonify,render_template
import pandas as pd
import pickle
app=Flask(__name__)

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

@app.route('/predict',methods=['POST'])
def get_prediction():
    baby_data_form=request.form
    baby_data_cleaned=get_cleaned_data(baby_data_form)
    baby_df=pd.DataFrame(baby_data_cleaned)
    with open("model1.pkl","rb") as obj:
        model=pickle.load(obj)
    prediction=model.predict(baby_df)
    prediction=round(float(prediction),2)
    response={"prediction":prediction}
    return render_template('index.html',prediction=prediction)


if __name__=='__main__':
    app.run(debug=True)