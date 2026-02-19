from flask import Flask, session, redirect, url_for, request,render_template
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
app.secret_key = "jr8665lk"

class User(db.Model):   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    password = db.Column(db.String(50))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")

        new_user = User(name=name, password=password)
        db.session.add(new_user)
        db.session.commit()

        return "User added successfully"

    return '''
        <form method="POST">
            Name: <input type="text" name="name"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Add User">
        </form>
    '''

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        users = User.query.filter_by(name=name, password=password).first()
        if users: 
            session["user"] = users.name  
            if 'user' in session:
                return redirect(url_for("dashboard"))
        else:
            return "Invalid Username or Password"

    return '''
    <form method="POST">
      Name: <input type="text" name="name"><br>
      Password: <input type="password" name="password"><br>
      <input type="submit">
    </form>
    '''

@app.route("/dashboard")
def dashboard():
    if "user" in session:   
        return f"Welcome to the dashboard {session['user']}"
        
    return "User session is off"

@app.route("/logout")
def logout():
    session.pop("user")
    return "User logged out successfully"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
