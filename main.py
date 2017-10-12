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

    body = db.Column(db.String(120))



    def __init__(self, title, body):

        self.title = title
        self.body = body

    def __repr__(self):
        return '<title %r>' % self.title

    def __repr__(self):
        return '<body %r>' % self.body


def get_current_blogs():
    return Blog.query.filter_by(title=True).all()


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    #use a 'GET' to go to the database to retreive the current submitted Blogs so they will be displayed on the main blog page. this is just a list of the blogs.
    title_name = request.form['title']

    body_content = request.form['body']

    new_tile = Blog(title_name)

    new_body = Blog(body_content)

    db.session.add(new_title, body_content)

    db.session.commit()

    blogs = Task.query.filter_by(title=False).all()
    completed_blogs = Task.query.filter_by(title=True).all()

@app.route('/newpost', methods=['POST'])
def new_post():
    if request.method == 'POST':

        title = request.form['title']
        body = request.form['body']
        title_err = ''
        body_err = ''

        if new_post_title == '':
            title_err = "Please enter a valid Title"
    
        if new_post_body == '':
            body_err = "Please enter a valid blog post"

    

        blog = Blog(title, body)
        db.session.add(blog)
        db.session.commit()

        return redirect('/blog', title=title, body=body, body_err=body_err, title_err=title_err)


    else:
        return render_template('newpost.html')

    @app.route('/')
    def index():
        encoded_error = request.args.get("error")
        return render_template('blog.html', encoded_error=error, blog_list=get_current_blogs())


if __name__ == '__main__':

    app.run()