from flask import Flask, render_template, request, redirect
import pyrebase

app = Flask(__name__)
app.secret_key = "CARPE"

firebaseConfig = {
    'apiKey': "AIzaSyBOh36Nz1q1dMu7LHrpj-FAR0nT2O9Nwdg",
    'authDomain': "carpe-c0b43.firebaseapp.com",
    'databaseURL': "https://carpe-c0b43.firebaseio.com",
    'projectId': "carpe-c0b43",
    'storageBucket': "carpe-c0b43.appspot.com",
    'messagingSenderId': "430812294648",
    'appId': "1:430812294648:web:eca4c668287162b02c3a0d",
    'measurementId': "G-WNYMY8MF2W"
}


firebase = pyrebase.initialize_app(firebaseConfig)
database = firebase.database()
storage = firebase.storage()
auth = firebase.auth()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_login = auth.sign_in_with_email_and_password(
            request.form['email'].strip(), request.form['password'])
        return redirect('/')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        user = auth.create_user_with_email_and_password(
            request.form['email'], request.form['password'])
    return render_template('register.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
