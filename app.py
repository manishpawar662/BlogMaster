from flask import Flask, render_template, request, redirect, jsonify,flash,session,url_for
from datetime import datetime
import os
import json
app = Flask(__name__)
from flask import Flask
import os
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash,generate_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


#mysql config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_upassword']='Manish@#123'
app.config['MYSQL_DB'] = 'blog_flask'
app.secret_key = '44d7efa5895341b3b719387b3089c21f'
mysql= MySQL(app)

@app.route('/home',methods=['GET','POST'])
def home():
    if user_in_session():
        username = session['username']
        posts = fetchposts()
        # conn.close() 
        return render_template("home.html", username=username, posts= fetchposts())
    else:
        flash("Try logging in", 'error')
        return redirect(url_for('login'))


@app.route('/postspage', methods=['GET', 'POST'])
def postspage():
    if user_in_session():
        username = session['username']
        return render_template('postspage.html', username=username, posts=fetchposts(), comments=fetchcomments())
    return redirect('/login')

# /<string:table>/<int:sno>


@app.route('/deletepost/<int:sno>', methods=['GET', 'POST'])
def deletepost(sno):
    if not (user_in_session()):
        # Redirect to login page if username is not in session
        return redirect("/login")
    print("sno----->",sno)
    if request.method:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM posts WHERE sno=%s", (sno,))
        mysql.connection.commit()  # Commit the transaction
        cur.close()
        flash("Post deleted succesfully", 'success')
    return redirect("/postspage")

@app.route('/deletecomment/<int:sno>', methods=['GET', 'POST'])
def deletecomment(sno):
    if not (user_in_session()):
        # Redirect to login page if username is not in session
        return redirect("/login")
    print("sno----->",sno)
    if request.method:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM comments WHERE sno=%s", (sno,))
        mysql.connection.commit()  # Commit the transaction
        cur.close()
        flash("Comment deleted succesfully", 'success')
    return redirect("/postspage")


@app.route('/',methods=['GET','POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT username, password FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and user[1] == password:
            session['username'] = user[0]
            flash("Login Successfully", 'success')
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password'
            flash("Username or password is incorrect", 'error')
            return render_template('login.html')
            # return render_template('login.html',error=error)
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, username, email, password) VALUES (%s, %s, %s, %s)", (name, username, email, password))
        mysql.connection.commit()  # Commit the transaction
        cur.close()
        flash("SignUp Successfully", 'success')
        return redirect(url_for('login'))
    return render_template("signup.html")

@app.route('/postcontent', methods=['GET', 'POST'])
def postcontent():
    if not(user_in_session()):
        # Redirect to login page if username is not in session
        return redirect("/login")

    if request.method == 'POST':
        content = request.form['content']
        username = session['username']
        image = request.files['imdata']
        print(image)
        # Ensure a filename is present and secure it
        if image and image.filename != '':
            filename = secure_filename(image.filename)
# Save the file
            folder_path = os.path.join(os.path.dirname(__file__), 'static', 'postimages')
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            unique_file_name = datetime.now().strftime('%d_%m_%Y_%H_%M_%S') + '.jpg'
            image.save(os.path.join(folder_path, unique_file_name))
            
            # Insert product details into the database
            # conn = sqlite3.connect('Shopme-database.db')
            # cursor = conn.cursor()
            imdata = str(unique_file_name)
        # Print username to check if it's correctly set in the session
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO posts (username,content,imdata) VALUES (%s, %s,%s)", (username, content,imdata))
            mysql.connection.commit()  # Commit the transaction
            cur.close()
            # flash("Post added Successfully", 'success')
    return redirect("/home")

@app.route('/addcomment/<current_user>/<post_username>/<post_sno>', methods=['POST', 'GET'])
def addcomment(current_user, post_username, post_sno):
    # Your comment adding logic here
    print(f'{current_user} and {post_username} {post_sno} ')
    if request.method == 'POST' or request.method == 'GET':
        comment = request.form['commentcontent']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO comments (post_username, comment_username, post_sno, comment) VALUES (%s, %s, %s, %s)", (post_username, current_user, post_sno, comment))
        mysql.connection.commit()  # Commit the transaction
        cur.close()
        flash("comment added:)", 'success')
    return redirect('/postspage')
        
    #     return redirect(url_for('/posts'))
    # return redirect('/')
    
@app.route('/logout')
def logout():
    session.pop('username',None)
    flash("Logged out", 'info')
    return redirect(url_for('login'))

def fetchposts():
    cursor = mysql.connection.cursor()
    # Fetch posts from the database
    cursor.execute('SELECT * FROM posts')
    rows = cursor.fetchall()
    posts = []
    for row in rows:
        post = {
            'sno': row[0],
            'username': row[1],
            'content': row[2],
            'imdata':row[3]
        }
        posts.append(post)
        # Close database connection
    cursor.close()
    return posts

def fetchcomments():
    cursor = mysql.connection.cursor()
    # Fetch posts from the database
    cursor.execute('SELECT * FROM comments')
    rows = cursor.fetchall()
    comments = []
    for row in rows:
        comment = {
            'sno': row[0],
            'post_username': row[1],
            'comment_username': row[2],
            'post_sno': row[3],
            'comment': row[4],
        }
        comments.append(comment)
        # Close database connection
    cursor.close()
    return comments

def user_in_session():
    if 'username' in session:
        return True
    return False

# main function
if __name__ == '__main__':
    app.run(debug=True,port=3000)