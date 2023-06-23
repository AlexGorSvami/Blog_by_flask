from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/write-blog/', methods=['GET', 'POST'])
def write_blog():
    return render_template('write-blog.html')

@app.route('/my-blogs/')
def my_blogs():
    return render_template('my-blogs.html')
@app.route('/blogs/<int:id>')
def blogs(id):
    return render_template('blogs.html', blog_id=id)

@app.route('/edit-blog/<int:id>', methods=['GET', 'POST'])
def edit_blog(id):
    return render_template('edit-blog.html', blog_id=id)

@app.route('/delete-blog/', methods=['POST'])
def delete_blog(id):
    return 'Deleted successfully'

@app.route('/register/',  methods=['POST', 'GET'])
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)

