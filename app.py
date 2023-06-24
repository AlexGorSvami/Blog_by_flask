import os

import yaml
from flask import Flask, render_template, flash, session, request, redirect
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_ckeditor import CKEditor

app = Flask(__name__)
Bootstrap(app)
CKEditor(app)

db = yaml.full_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = os.urandom(24)
mysql = MySQL(app)
@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    result_value = cursor.execute('SELECT * FROM blog')
    if result_value > 0:
        blogs = cursor.fetchall()
        cursor.close()
        return render_template('index.html', blogs=blogs)
    return render_template('index.html', blogs=None)

@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_inform = request.form
        username = user_inform['username']
        cursor = mysql.connection.cursor()
        result_value = cursor.execute("SELECT * FROM user WHERE username = %s", ([username]))
        if result_value > 0:
            user = cursor.fetchone()
            if check_password_hash(user['password'], user_inform['password']):
                session['login'] = True
                session['first_name'] = user['first_name']
                session['last_name'] = user['last_name']
                flash(f"Welcome {session['first_name']}! You have been successfully logged in!", 'success')
            else:
                cursor.close()
                flash('Password is incorrect', 'danger')
                return render_template('/login/')
        else:
            cursor.close()
            flash('User does not exist', 'danger')
            return render_template('/login/')
        cursor.close()
        return redirect('/')
    return render_template('login.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')


@app.route('/write-blog/', methods=['GET', 'POST'])
def write_blog():
    if request.method == 'POST':
        blogpost = request.form
        title = blogpost['title']
        body = blogpost['body']
        author = f"{session['first_name']} {session['last_name']}"
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO blog (title, body, author) VALUES (%s, %s, %s)", (title, body, author))
        mysql.connection.commit()
        cursor.close()
        flash('Your post is successfully saved', 'success')
        return redirect('/')
    return render_template('write-blog.html')

@app.route('/my-blogs/')
def my_blogs():
    return render_template('my-blogs.html')
@app.route('/blogs/<int:id>')
def blogs(id):
    cursor = mysql.connection.cursor()
    result_value = cursor.execute("SELECT * FROM blog WHERE blog_id = {}".format(id))
    if result_value > 0:
        blog = cursor.fetchone()
        return render_template('blogs.html', blog=blog)
    return 'Blog is not found'

@app.route('/edit-blog/<int:id>', methods=['GET', 'POST'])
def edit_blog(id):
    return render_template('edit-blog.html', blog_id=id)

@app.route('/delete-blog/', methods=['POST'])
def delete_blog(id):
    return 'Deleted successfully'

@app.route('/register/',  methods=['GET',  'POST'])
def register():
    if request.method == 'POST':
        user_inform = request.form
        if user_inform['password'] != user_inform['confirmPassword']:
            flash("Passwords don't match! Try again!", 'danger')
            return render_template('register.html')
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO user(first_name, last_name, username, email, password) VALUES (%s, %s, %s, %s, %s)",
        (user_inform['firstname'], user_inform['lastname'], user_inform['username'], user_inform['email'],
        generate_password_hash(user_inform['password'])))
        mysql.connection.commit()
        cursor.close()
        flash('Registration successful! Please enter your login!', 'success')
        return redirect('/login/')
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)

