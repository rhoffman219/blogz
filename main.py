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

@app.before_request
def require_login():
    allowed_routes = ['blog', 'login', 'signup', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')       

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(20000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        
        self.title = title
        self.body = body
        self.owner = owner       

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        blog_title = request.form['title']
        owner = User.query.filter_by(username=session['username']).first()
        new_blog = Blog(blog_title, owner)
        db.session.add(new_blog)
        db.session.commit()

    
    return render_template('index.html')


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
        owner = User.query.filter_by(username=session['username']).first()

        if title == '' or body == '':
            title_err = "Please enter a valid title"
            body_err = "Please enter text into your blog"
            return render_template('newpost.html', title_err=title_err, body_err=body_err)

        else:
            blog = Blog(title, body, owner)
            db.session.add(blog)
            db.session.commit()
            return redirect('/blog?id=' + str(blog.id))

    return render_template('newpost.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    username_err = ''
    password_err = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if username == '' or password == '':
            username_err = 'Please enter a valid username'
            password_err = 'Please enter a valid password'
            return render_template('login.html', username_err=username_err, password_err=password_err)
        
        if user and user.password == password:
            session['username'] = username
            return redirect('/newpost')
    
        else:
            username_err = 'User does not exist! Please register to logon!'
            return render_template('login.html', username_err=username_err)
        
    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    username_err = ''
    verify_err = ''
    password_err = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        #TODO: need to validate user's data above. 
        existing_user = User.query.filter_by(username=username).first()
        
        if username == '' or password == '' or verify == '':
            username_err = 'Please enter a valid email'
            password_err = 'Please enter a valid password'
            verify_err = 'Please verify password'
            return render_template('signup.html', username_err=username_err, password_err=password_err, verify_err=verify_err)

        if '@' not in username or '.' not in username or ' ' in username:
            username_err = 'Please enter a valid email'
            return render_template('signup.html', username_err=username_err)
        
        if existing_user:  
            username_err = 'This user already exists! Please login'
            return render_template('signup.html', username_err=username_err)
        
        if not verify == password:
            verify_err = 'Your passwords do not match!'
            return render_template('signup.html', verify_err=verify_err) 

        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')

    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

        





if __name__ == '__main__':



    app.run()