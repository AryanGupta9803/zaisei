from flask import Flask, render_template, redirect, request
import firebase_admin
from firebase_admin import credentials, auth

app = Flask(__name__)

cred = credentials.Certificate('zaisei-kuhaku-firebase-adminsdk-534l6-98bbc60897.json')
firebase_admin.initialize_app(cred)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.create_user(email=email, password=password)
            # User creation successful
            # You can redirect to a different page or perform other actions
            return redirect('/login')
        except auth.AuthError as e:
            error_message = str(e)
            return render_template('signup.html', error=error_message)
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.get_user_by_email(email)
            auth.verify_password(email, password)
            # Authentication successful
            # You can redirect to a different page or perform other actions
            return redirect('/dashboard')
        except auth.AuthError as e:
            error_message = str(e)
            return render_template('login.html', error=error_message)
    return render_template('login.html')


