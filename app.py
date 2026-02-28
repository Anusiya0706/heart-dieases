from flask import Flask, render_template, request, redirect, url_for
import pymysql

app =Flask(__name__)

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    msg=''
    output=""
    if request.method == 'POST':
        age = int(request.form['age'])
        sex =int(request.form['sex'])
        cp= int(request.form['cp'])
        trestbps = int(request.form['trestbps'])
        chol = int(request.form['chol'])
        fbs =int(request.form['fbs'])
        restecg =int(request.form['restecg'])
        thalach =int(request.form['thalach'])
        exang =int(request.form['exang'])
        oldpeak =float(request.form['oldpeak'])
        slope =int(request.form['slope'])
        ca =int(request.form['ca'])
        thal =int(request.form['thal'])
        test_data=[age, sex, cp, trestbps, chol,fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
        print("test data",test_data)
        import pandas as pd
        from sklearn.model_selection import train_test_split
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import accuracy_score
        
        data = pd.read_csv("heart.csv")
        data.head()

        data.info()

        X= data.drop('target', axis=1)
        Y= data['target']

        X_train, X_test, Y_train, Y_test =train_test_split(X, Y, test_size=0.2)

        model =RandomForestClassifier(n_estimators=100, random_state=42)

        model.fit(X_train, Y_train)

        Predictions =model.predict([test_data])
        print(Predictions)

        if(Predictions[0]==0):
                print("No Heart Disease")
                output="No Heart Disease"
        else:
                print("Heart Disease")
                output=" Heart Disease" 
                 
    return render_template('Heart_Disease_Prediction.html',msg=msg,output=output,Title="Heart_Disease_Prediction") 
@app.route('/', methods=['GET', 'POST'])
def SignUp():  
    msg =''
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']

        mydb= pymysql.connect(
        host='localhost',  
        user='root',
        password='root',
        database='heart'
        )
        print("Username", email)
        print("password", password)
        mycursor = mydb.cursor()
        sql="Insert Into register (email, password) Values (%s, %s)"
        val=(email, password)
        mycursor.execute(sql, val)
        mydb.commit()
        print("1 record inserted, ID:", mycursor.lastrowid)
        msg="Record successfully inserted"
        return render_template('login.html', msg=msg)

    return render_template('signup.html', msg=msg)
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST': 
        email = request.form['email']   
        password = request.form['password']
        print(email, password)
        mydb= pymysql.connect(
        host='localhost',  # e.g., 'localhost' or an IP address
        user='root',
        password='root',
        database='heart'
        )
        cursor = mydb.cursor()
        cursor.execute('select count(*) from register where email=%s and password=%s', (email, password))
        count = cursor.fetchone()[0]
        cursor.close()
        if count > 0:
            msg = 'Login Success'
            return render_template('Heart_Disease_Prediction.html', msg=msg)
        else:
            msg = 'Login failed'
            return render_template('login.html', msg=msg)
    # For GET requests, show the login page
    return render_template('login.html', msg=msg)
if __name__=='__main__':
    app.run(port=5000,debug=True)