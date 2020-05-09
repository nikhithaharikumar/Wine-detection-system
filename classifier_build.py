import numpy as np
import os
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pandas
from flask import Flask,render_template, request, redirect, url_for, Blueprint, send_file, jsonify,session,Response
from database import db_connect,  user_reg,user_loginact
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from io import BytesIO
import base64
import re

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

@app.route("/view",methods=['GET','POST'])
def view():
    # reads the contents of the uploaded file by the user
    data=pandas.read_csv(request.files.get('file'))
    peek=data.head(30)
    return render_template("view.html",tables=[peek.to_html(classes='data')])


@app.route("/userreg", methods = ['GET','POST'])
def userreg():
   if request.method == 'POST':
        #regular expression to check email validity
        regex_email = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        messages = []
        if not re.search(regex_email,request.form['email']):
           messages.append("Invalid Email Format.")
        if len(request.form['password'])!= 8:
            messages.append("Password should be minimum 8 characters.")
        if request.form['password'] != request.form['confirm_password']:
            messages.append("The passwords don't match.")
        if len(str(request.form['mobile']))!=10:
            messages.append("Mobile number should be 10 digits long.")
        if messages:
            return render_template("register.html",messages=messages)
        results = user_reg(request.form['username'],request.form['email'],request.form['password'],request.form['address'],request.form['mobile'])
        if results != []:
            return render_template("login.html",m1="success")
        else:
            return render_template("register.html",messages="failed")



@app.route("/userlogact", methods=['GET', 'POST'])       
def userlogact():
        if request.method == 'POST':
           results = user_loginact(request.form['username'], request.form['password'])
           print(results)
        if results != []:
            session['username'] = request.form['username']
            return render_template("userhome.html", message="success",username =request.form['username'])
        else:
            return render_template("login.html", message="Invalid Credentials !! Please Try Again")

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

    red_wine = [[fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides, free_sulfur_dioxide,
                 total_sulfur_dioxide, density, pH, sulphates, alcohol]]

    wine = [fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides, free_sulfur_dioxide,
            total_sulfur_dioxide, density, pH, sulphates, alcohol]
    index = ['fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar', 'chlorides', 'free_sulfur_dioxide',
             'total_sulfur_dioxide', 'density', 'pH', 'sulphates', 'alcohol']

    df = pandas.DataFrame({'red_wine': wine}, index=index)
    df.plot.barh(y='red_wine', color='r')
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.tight_layout()

    img = BytesIO()

    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    ### Dataset as df
    dataset = pandas.read_csv('winequality-red.csv')

    ### Shuffle data
    from sklearn.utils import shuffle
    dataset = shuffle(dataset)

    ### Separate label y from features X
    X = dataset.iloc[:, :11].values
    y = dataset.iloc[:, 11].values

    ### Standardize features
    from sklearn.preprocessing import StandardScaler
    sc_X = StandardScaler()
    X = sc_X.fit_transform(X)

    ### Train/Validation/Test split
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    ################################### MODELS ################################################################################################

    ### Logisitic Regression
    from sklearn.linear_model import LogisticRegression
    classifier_log = LogisticRegression()
    classifier_log.fit(X_train, y_train)
    pred = classifier_log.predict(red_wine)
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxx predicted value xxxxxxxxxxxxxxxxxxx")
    print(pred)
    quality = dataset["quality"].values
    category = []

    return render_template("result.html", pred=pred, plot_url=plot_url)

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)