from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
scaler=StandardScaler()
untitled0=Flask(__name__)
model=pickle.load(open('model_randomforest.pkl','rb'))
@untitled0.route('/',methods=['GET'])

def Home():
    return render_template('index.html')

@untitled0.route('/predict',methods=['POST'])
def predict():
    Fuel_type_Diesel=0
    if request.method=='POST':
        Year=int(request.form['Year'])
        Present_Price=int(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Owner=int(request.form['Owner'])
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if Fuel_Type_Petrol=='Petrol':
            Fuel_Type_Petrol=1
            Fuel_type_Diesel=0
        elif Fuel_Type_Petrol=='Diesel':
            Fuel_Type_Petrol=0
            Fuel_type_Diesel=1
        else:
            Fuel_Type_Petrol=0
            Fuel_type_Diesel=0
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if Seller_Type_Individual=='Individual':
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0
        Transmission_Mannual=request.form['Transmission_Mannual']
        if Transmission_Mannual=='Mannual':
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0
        predictions=model.predict([[Present_Price, Kms_Driven, Owner, 
                                    Year,Fuel_type_Diesel,
                                    Fuel_Type_Petrol,
                                    Seller_Type_Individual,
                                    Transmission_Mannual]])
        output=round(predictions[0],2)
        if output<0:
            return render_template('index.html', 
                                   prediction_texts='You can''t Sell the Car')
        else:
            return render_template('index.html',
                                   prediction_texts='You Selled a car at {}'.format(output))
    else:
        return render_template('index.html')
if __name__=='__main__':
    untitled0.run(debug=True)
        