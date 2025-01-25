from flask import Flask, render_template, request, redirect, jsonify, flash, session, url_for
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///MediaDb.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
# Get the absolute path of the current directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# Set the secret key to something unique and secret
app.config['SECRET_KEY'] = os.urandom(24)

# Define the new database URI
db_uri = f'sqlite:///{os.path.join(BASE_DIR, "MediaDb.db")}'

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

# Define the database models

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

class Post(db.Model):
    __tablename__ = 'posts'
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    imdata = db.Column(db.String(100))

class Comment(db.Model):
    __tablename__ = 'comments'
    sno = db.Column(db.Integer, primary_key=True)
    post_username = db.Column(db.String(100), nullable=False)
    comment_username = db.Column(db.String(100), nullable=False)
    post_sno = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)

# Route to home page after login
@app.route('/home', methods=['GET', 'POST'])
def home():
    if user_in_session():
        username = session['username']
        posts = fetchposts()
        return render_template("home.html", username=username, posts=posts)
    else:
        flash("Try logging in", 'error')
        return redirect(url_for('login'))

# Route to the posts page
@app.route('/postspage', methods=['GET', 'POST'])
def postspage():
    if user_in_session():
        username = session['username']
        return render_template('postspage.html', username=username, posts=fetchposts(), comments=fetchcomments())
    return redirect('/login')

# Route to delete a post
@app.route('/deletepost/<int:sno>', methods=['GET', 'POST'])
def deletepost(sno):
    if not user_in_session():
        return redirect("/login")

    post = Post.query.get(sno)
    if post:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully", 'success')
    return redirect("/postspage")

# Route to delete a comment
@app.route('/deletecomment/<int:sno>', methods=['GET', 'POST'])
def deletecomment(sno):
    if not user_in_session():
        return redirect("/login")

    comment = Comment.query.get(sno)
    if comment:
        db.session.delete(comment)
        db.session.commit()
        flash("Comment deleted successfully", 'success')
    return redirect("/postspage")

# Route for login page
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            session['username'] = user.username
            flash("Login Successful", 'success')
            return redirect(url_for('home'))
        else:
            flash("Username or password is incorrect", 'error')
            return render_template('login.html')
    return render_template('login.html')

# Route for signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name=name, username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash("SignUp Successful", 'success')
        return redirect(url_for('login'))

    return render_template("signup.html")

# Route for adding content to a post
@app.route('/postcontent', methods=['GET', 'POST'])
def postcontent():
    if not user_in_session():
        return redirect("/login")

    if request.method == 'POST':
        content = request.form['content']
        username = session['username']
        image = request.files['imdata']

        if image and image.filename != '':
            filename = secure_filename(image.filename)
            folder_path = os.path.join(os.path.dirname(__file__), 'static', 'postimages')
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            unique_file_name = datetime.now().strftime('%d_%m_%Y_%H_%M_%S') + '.jpg'
            image.save(os.path.join(folder_path, unique_file_name))

            new_post = Post(username=username, content=content, imdata=unique_file_name)
            db.session.add(new_post)
            db.session.commit()

        return redirect("/home")

# Route for adding a comment to a post
@app.route('/addcomment/<current_user>/<post_username>/<post_sno>', methods=['POST', 'GET'])
def addcomment(current_user, post_username, post_sno):
    if request.method == 'POST' or request.method == 'GET':
        comment = request.form['commentcontent']

        new_comment = Comment(post_username=post_username, comment_username=current_user,
                              post_sno=post_sno, comment=comment)

        db.session.add(new_comment)
        db.session.commit()
        flash("Comment added successfully", 'success')

    return redirect('/postspage')

# Route for logging out
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out", 'info')
    return redirect(url_for('login'))

# Function to fetch posts
def fetchposts():
    posts = Post.query.all()
    post_list = [{'sno': post.sno, 'username': post.username, 'content': post.content, 'imdata': post.imdata} for post in posts]
    return post_list

# Function to fetch comments
def fetchcomments():
    comments = Comment.query.all()
    comment_list = [{'sno': comment.sno, 'post_username': comment.post_username, 'comment_username': comment.comment_username,
                     'post_sno': comment.post_sno, 'comment': comment.comment} for comment in comments]
    return comment_list

# Function to check if a user is in session
def user_in_session():
    return 'username' in session


# Create all the tables if they don't exist yet
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
