from flask import Flask, request, redirect, render_template



from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(20000))

    def __init__(self, title, body):

        self.title = title

        self.body = body

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        title_name = request.form['title']
        new_title = Blog(title_name)
        db.session.add(new_title)
        db.session.commit()

    titles = Blog.query.all()
    return render_template('blog.html',title="Blogs!", titles=titles)

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    if request.method == "POST":
        title_name = request.form['title']
        body_content = request.form['body']
        new_title = Blog(title_name)
        new_body_content = Blog(body_content)
        db.session.add(new_title, new_body_content)
        db.session.commit()

@app.route('/newpost', methods=['GET', 'POST'])
def new_post():

    if request.method == 'POST': 
        title = request.form['title']
        body = request.form['body']
        title_err = ''
        body_err = ''   

        if title == '':

            title_err = "Please enter a valid Title"

        elif body == '':

            body_err = "Please enter a valid blog post"

        if not title_err or not body_err:
            blog = Blog(title, body)

            db.session.add(blog)

            db.session.commit()

            return render_template('blog.html', title=title, body=body)   
        
    
    
        else:

            return render_template('newpost.html', title_err=title_err, body_err=body_err, title=title, body=body)



        





if __name__ == '__main__':



    app.run()