from flask import Flask, render_template, request, redirect, session
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
    if(session['logged_in']):
        users = []
        users = database.child("users").get().val()
        projects = []
        projects = database.child("project").get().val()
        session["users"] = []
        session["projects"] = []
        for project in projects.values():
            session["projects"].append(project)
        for user in users.values():
            session["users"].append(user)
        return render_template('index.html')
    else:
        return redirect('/login')


@app.route('/projects')
def projects():
    return render_template('add_project.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['logged_in'] = True
        user_login = auth.sign_in_with_email_and_password(
            request.form['email'].strip(), request.form['password'])
        users = []
        users = database.child("users").get().val()
        projects = []
        projects = database.child("project").get().val()
        session["users"] = []
        session["projects"] = []
        for project in projects.values():
            session["projects"].append(project)
        print(session['projects'])
        # print(auth.get_account_info(user_login['idToken']))

        for user in users.values():
            session["users"].append(user)
            # print(user['primary_key'] == user_login['idToken'])
            if(user['email'] == request.form['email']):
                session["user"] = user.copy()
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
        folder_name = request.form['fname']+request.form['lname'] + \
            str(auth.get_account_info(user['idToken'])['users'][0]['localId'])
        database.child("users").child(folder_name).update({
            'fname': request.form['fname'],
            'lname': request.form['lname'],
            'email': request.form['email'],
            'roles': request.form['roles']
        })
        return redirect('/login')
    return render_template('register.html')


@app.route('/add_project', methods=['POST', 'GET'])
def add_project():
    if request.method == 'POST':
        project_name = request.form['project_name']
        project_location = request.form['project_location']
        project_form_link = request.form['project_form_link']
        employees = [session["user"]['fname'] + " " + session["user"]['lname']]
        project = {
            'project_name': project_name,
            'project_location': project_location,
            'project_form_link': project_form_link,
            'employees': employees
        }
        database.child('project').child(
            project_name+project_location).update(project)
        return redirect('/')


@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        employee_name = request.form['employee_name']
        project_name = request.form['project_name']
        proj = {}

        for project in session['projects']:

            if project['project_name'] == project_name:
                proj = project.copy()
        employees = database.child('project').child(
            proj['project_name']+proj['project_location']).child('employees').get().val()
        employees.append(employee_name)
        database.child('project').child(
            proj['project_name']+proj['project_location']).update({'employees': employees})
        return redirect('/')
    return render_template('/add_employee.html')


@app.route('/logout')
def logout():
    session.pop("user", None)
    session['logged_in'] = False
    return redirect('/home')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
