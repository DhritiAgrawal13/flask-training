from flask import Flask,render_template,url_for,request,redirect,flash,session
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db=SQLAlchemy(app)
app.secret_key = "jr8665lk"

class user(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(40))
    password=db.Column(db.String(50),nullable=False)
@app.route('/')
def home():
    return render_template('welcome.html')
@app.route('/add',methods=['GET,POST'])
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        if name and password:
            new_user = user(name=name, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('User added successfully', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Please fill all fields', 'error')

    return '''
        <form method="POST">
            Name: <input type="text" name="name" placeholder="enter name"><br><br>
            Password: <input type="password" name="password" placeholder="enter password"><br><br>
            <input type="submit" value="Add User">
        </form>
    '''
def dashboard():
    return f"welcome to the dashboard {user.name}"



if(__name__=="__main__"):
    with app.app_context():
        db.create_all()
    app.run(debug=True)