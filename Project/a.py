from flask import Flask, redirect, render_template, session, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'jri5iht'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(60), nullable=False)

class Feedback_Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.String(50), nullable=False)

@app.route('/')
def home():
    return "Welcome to our Feedback Collection System"

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form.get('Name')
        password = request.form.get('Password')
        email = request.form.get('Email')
        if not email.endswith('@gmail.com'):
            return "gmail format is wrong"
        new_user = User(name=name, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()
        return "User added successfully"
    return render_template('user_add.html')

@app.route('/add_feedback', methods=['GET', 'POST'])
def add_feedback():
    if "user" not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form.get('Name')
        comment = request.form.get('Comment')
        rating = request.form.get('Rating')
        new_feedback = Feedback_Form(name=name, comment=comment, rating=rating)
        db.session.add(new_feedback)
        db.session.commit()
        return "Feedback added successfully"
    return render_template('feedback.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        user = User.query.filter_by(name=name, password=password).first()
        if user:
            session['user'] = user.name
            a=session['user']
            return render_template('dashborad.html',a=a)
        return "User does not exist"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if "user" not in session:
        return redirect(url_for('login'))
    return render_template('dashborad.html')

@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user():
    if "user" not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        id = request.form.get('id')
        user = User.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return "User deleted successfully"
        return "User does not exist"
    return render_template('delete.html')

@app.route('/feedback_delete', methods=['GET', 'POST'])
def feedback_delete():
    if "user" not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        id = request.form.get('id')
        feedback = Feedback_Form.query.get(id)
        if feedback:
            db.session.delete(feedback)
            db.session.commit()
            return "Feedback deleted successfully"
        return "Feedback post  not found"

    return render_template('delete_feedback.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return "Logged out successfully"

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if "user" not in session:
        return redirect(url_for('login'))

    user = User.query.get(id)
    if not user:
        return "User not found"

    if request.method == 'POST':
        user.name = request.form.get('name')
        user.email = request.form.get('email')
        user.password = request.form.get('password')
        db.session.commit()
        return "User updated successfully"

    return render_template('update2.html', user=user)

@app.route('/show_user')
def show_user():
    if "user" not in session:
        return redirect(url_for('login'))
    users = User.query.all()
    return render_template('show_user.html', users=users)

@app.route('/show_feedback')
def show_feedback():
    if "user" not in session:
        return redirect(url_for('login'))
    feedbacks = Feedback_Form.query.all()
    return render_template('show_feedback.html', feedbacks=feedbacks)

@app.route('/rating')
def rating():
    if "user" not in session:
        return render_template('login.html')
    f=User.query.order_by(User.rating.asc()).all()
    return render_template('/rating.html',f=f)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
