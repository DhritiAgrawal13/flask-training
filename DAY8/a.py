from flask import Flask, session, redirect, url_for, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test2.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "jr8665lk"

db = SQLAlchemy(app)

class User(db.Model):   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50))
    title = db.Column(db.String(50))
    role = db.Column(db.String(50))
    status = db.Column(db.String(50))

@app.route('/')
def home():
    return render_template('user.html')

@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        user = User.query.filter_by(name=name, password=password).first()
        new_user = User(name=name, password=password)
        if not user:
            db.session.add(new_user)
            db.session.commit()
            flash("User registered successfully", "success")
            return "user successfully added in the system"
        return "user already in the system"
    return render_template("index.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        user = User.query.filter_by(name=name, password=password).first()
        if user:
            session["user"] = user.name
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid Username or Password", "danger")

    return render_template("login.html")

@app.route('/show_data')
def show_data():
    users = User.query.all()
    return render_template('table.html', users=users)

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return f"Welcome to Dashboard, {session['user']}"
    return redirect(url_for("login"))

@app.route('/post', methods=['GET', 'POST'])
def create_post():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form.get("Title")
        role = request.form.get("Role")
        status = request.form.get("Status")

        new_post = Post(
            title=title,
            user=session["user"],
            role=role,
            status=status
        )

        db.session.add(new_post)
        db.session.commit()

        return "Post created successfully"

    return render_template('post.html')

@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user():
    if request.method == "POST":
        user_id = request.form.get("id")
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return "User deleted successfully"
        else:
            return f"User does not exist {type(user_id)}"

    return render_template('delete_user.html')

@app.route('/show_post')
def show_post():
    users = Post.query.all()
    return render_template('show_post.html',user=users)


@app.route('/delete_post', methods=['GET', 'POST'])
def delete_post():
    if request.method == "POST":
        post_id = request.form.get("id")

        post = Post.query.get(post_id)

        if post:
            db.session.delete(post)
            db.session.commit()
            return "Post deleted successfully"
        else:
            return "Post does not exist"

    return render_template('delete_post.html')

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
