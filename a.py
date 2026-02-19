
from flask import Flask, render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    role = db.Column(db.String(20))
    email = db.Column(db.String(40),unique=True,nullable=False)
    posts = db.relationship('Post', backref='user', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(20))
    role = db.Column(db.String(20))
    email = db.Column(db.String(40))

@app.route('/')
def home():
    return "Flask + SQLAlchemy Working"

@app.route('/add')
def add():
    user = User(name="Amit", role="Admin", email="amit@gmail.com")
    try:  
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return f"email already exist {e}"
    return "<p> User Added Successfully! <p>"

@app.route('/adds')
def adds():
    user = User(name="Dhriti", role="Software Engineer", email="dhritiagrawal13@gmail.com")
    db.session.add(user)
    db.session.commit()

    post = Post(
        user_id=user.id,
        name="Dhriti",
        role="Software Engineer",
        email="dhritiagrawal13@gmail.com"
    )
    db.session.add(post)
    db.session.commit()

    return f"name={post.name}, role={post.role}"
@app.route('/posts')
def posts():
    page=request.args.get(page,1,type=int)
    posts=db.session.query(User,Post)\
    .join(User,Post.user_id==User.id)\
    .paginate(page=page,per_page=2)
    return render_template('home.html',posts=posts)
    

@app.route('/show/<int:user_id>')
def show(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return f"{user.name} - {user.role} - {user.email}"
    return "User Not Found"

@app.route('/delete/<int:user_id>')
def delete(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return "User Deleted"
    return "User Not Found"

@app.route('/show_all')
def show_all():
    users = User.query.all()
    return render_template("index.html", users=users)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
