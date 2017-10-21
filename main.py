from flask import Flask, request, redirect, render_template, flash, session



from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "ilovesuperheros"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(20000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body):
        
        self.title = title
        
        self.body = body
        self.owner = owner

@app.route('/')
def index():

    blogs = Blog.query.all()

    
    return render_template('blog.html', blogs=blogs)


@app.route('/blog', methods=['POST', 'GET'])
def blog():

    if request.args:
        id = request.args.get('id')
        blog = Blog.query.get(id)

        return render_template('singleblog.html', blog=blog)

    else:
        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs)

@app.route('/newpost', methods=['GET', 'POST'])
def new_post():
    title_err = ''
    body_err = ''

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        

        if title == '' or body == '':
            title_err = "Please enter a valid title"
            body_err = "Please enter text into your blog"
            return render_template('newpost.html', title_err=title_err, body_err=body_err)

        else:
            blog = Blog(title, body)
            db.session.add(blog)
            db.session.commit()
            return redirect('/blog?id=' + str(blog.id))

    return render_template('newpost.html')




        





if __name__ == '__main__':



    app.run()