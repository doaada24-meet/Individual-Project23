from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config={ "apiKey": "AIzaSyB1zEFErDoFQ6rTsHKcNiw8-XlRTBASdnc",
  "authDomain": "doaa-400f6.firebaseapp.com",
  "projectId": "doaa-400f6",
  "storageBucket": "doaa-400f6.appspot.com",
  "messagingSenderId": "165853957829",
  "appId": "1:165853957829:web:961a1d6501cf23e50eeaac",
  "databaseURL":"https://doaa-400f6-default-rtdb.europe-west1.firebasedatabase.app/"}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db=firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/signin',methods=['GET','POST'])
def signin():
     error = ""
     if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except Exception as e:
            error="Authentication failed"
        
            print(f"ERROR LOGGING IN: {e}")

     return render_template("signin.html")

@app.route('/signup',methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        fullname=request.form['full_name']
        username=request.form['username']
        bio=request.form['bio']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID=login_session['user']['localId']
            user={"full_name":fullname,"username":username,"bio":bio, "email": email}
            db.child("Users").child(UID).set(user)
            return redirect(url_for('map'))
        except Exception as e:
            error="Authentication failed"
            print(f"ERROR SIGNING UP: {e}")
    
    return render_template("signup.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/cards/<string:location>')
def cards(location):
    error=""
    if request.method == 'POST':
        image = request.form['card-image']
        title = request.form['title']
        description=request.form['description']
        location=request.form['location']
        try:
            user={"image":image,"title":title,"description":description, "location": location}
            db.child("Cards").push(user)
            return redirect(url_for('map'))
        except Exception as e:
            error="Authentication failed"
            print(f"ERROR SIGNING UP: {e}")
    return render_template("cards.html",location=location)

    
@app.route('/jordan/<string:location>')
def jordan(location):
    error=""
    if request.method == 'POST':
        image = request.form['card-image']
        title = request.form['title']
        description=request.form['description']
        location=request.form['location']
        try:
            user={"full_name":fullname,"username":username,"bio":bio, "email": email}
            return redirect(url_for('map'))
        except Exception as e:
            error="Authentication failed"
            print(f"ERROR SIGNING UP: {e}")
    return render_template("jordan.html",location=location)

@app.route('/map')
def map():
    UID = login_session['user']['localId']
    user = db.child("Users").child(UID).get().val()
    return render_template("map.html",username=user["username"])

if __name__ == '__main__':
    app.run(debug=True)