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

    body = db.Column(db.String(20,000))



    def __init__(self, title, body):

        self.title = title
        self.body = body







@app.route('/blog', methods=['POST', 'GET'])

def index():



    if request.method == 'POST':

        title_name = request.form['title']

        new_tile = Blog(title_name)

        db.session.add(new_title)

        db.session.commit()



    #title = Blog.query.all()

    #return render_template('blog.html', title=blog,title=title, body=body)
@app.route('/newpost', methods=['POST'])

def new_post():

    new_post_title = request.form('title')
    new_post_body = request.form('body')
    new_post_title_err = ''
    new_post_body_err = ''

    if new_post_title == '':
        new_post_title_err = "Please enter a valid Title"
    
    if new_post_body == '':
        new_post_body_err = "Please enter a valid blog post"



    return redirect('/blog')





if __name__ == '__main__':

    app.run()