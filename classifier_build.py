import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pandas
from flask import Flask,render_template, request, redirect, url_for, Blueprint, send_file, jsonify,session
from database import db_connect,  user_reg,user_loginact

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/")
def FUN_root():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/values")
def values():
    return render_template("values.html")

@app.route("/userhome")
def userhome():
    return render_template("userhome.html")

@app.route("/view")
def view():
    data=pandas.read_csv("C:\\Users\\home\\Documents\\Python\\wine prediction\\winequality-red.csv")
    peek=data.head(30)
    return render_template("view.html",tables=[peek.to_html(classes='data')])


@app.route("/userreg", methods = ['GET','POST'])
def userreg():
   if request.method == 'POST':      
      status = user_reg(request.form['username'],request.form['email'],request.form['password'],request.form['address'],request.form['mobile'])
      if status == 1:
       return render_template("login.html",m1="sucess")
      else:
       return render_template("register.html",m1="failed")


@app.route("/userlogact", methods=['GET', 'POST'])       
def userlogact():
        if request.method == 'POST':
           status = user_loginact(request.form['username'], request.form['password'])
           print(status)
        if status == 1:
            session['username'] = request.form['username']
            return render_template("userhome.html", m1="sucess")
        else:
            return render_template("login.html", m1="Login Failed")

@app.route('/rate', methods=['POST'])
def rate():
    #"""Gather User Input with conditioning for blank field"""
    if request.form['fixed_acidity'] == "":
        fixed_acidity = 8.32
    else:
        fixed_acidity = float(request.form['fixed_acidity'])

    if request.form['volatile_acidity'] == "":
        volatile_acidity = 0.53
    else:
        volatile_acidity = float(request.form['volatile_acidity'])

    if request.form['citric_acid'] == "":
        citric_acid = 0.27
    else:
        citric_acid = float(request.form['citric_acid'])

    if request.form['residual_sugar'] == "":
        residual_sugar = 2.54
    else:
        residual_sugar = float(request.form['residual_sugar'])

    if request.form['chlorides'] == "":
        chlorides = 0.09
    else:
        chlorides = float(request.form['chlorides'])

    if request.form['free_sulfur_dioxide'] == "":
        free_sulfur_dioxide = 15.87
    else:
        free_sulfur_dioxide = float(request.form['free_sulfur_dioxide'])

    if request.form['total_sulfur_dioxide'] == "":
        total_sulfur_dioxide = 46.47
    else:
        total_sulfur_dioxide = float(request.form['total_sulfur_dioxide'])

    if request.form['density'] == "":
        density = 1.00
    else:
        density = float(request.form['density'])

    if request.form['pH'] == "":
        pH = 3.31
    else:
        pH = float(request.form['pH'])

    if request.form['sulphates'] == "":
        sulphates = 0.66
    else:
        sulphates = float(request.form['sulphates'])

    if request.form['alcohol'] == "":
        alcohol = 10.42
    else:
        alcohol = float(request.form['alcohol'])

    red_wine = [[fixed_acidity, volatile_acidity, citric_acid, residual_sugar,
                 chlorides, free_sulfur_dioxide, total_sulfur_dioxide,
                 density, pH, sulphates, alcohol]]

    
### Dataset as df
    dataset = pandas.read_csv('winequality-red.csv')


### Shuffle data
    from sklearn.utils import shuffle
    dataset = shuffle(dataset)


    ### Separate label y from features X
    X = dataset.iloc[:,:11].values  
    y = dataset.iloc[:,11].values


    ### Standardize features
    from sklearn.preprocessing import StandardScaler
    sc_X = StandardScaler()
    X = sc_X.fit_transform(X)


    ### Train/Validation/Test split
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

    ################################### MODELS ################################################################################################

    ### Logisitic Regression
    from sklearn.linear_model import LogisticRegression
    classifier_log = LogisticRegression()
    classifier_log.fit(X_train,y_train)
    pred=classifier_log.predict(red_wine)
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxx predicted value xxxxxxxxxxxxxxxxxxx")
    print(pred)
    return render_template("result.html", pred=pred)

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)