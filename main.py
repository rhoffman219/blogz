from flask import Flask, request, redirect, render_template, flash, session



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

@app.route('/blog', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        title_name = request.form['title']
        new_title = Blog(title_name)
        db.session.add(new_title, body_content)
        db.session.commit()

    titles = Blog.query.all()
    return render_template('blog.html',title="Blogs!", titles=titles)

@app.route('/newpost', methods=['GET', 'POST'])
def new_post():

    if request.method == 'POST':



        title = request.form['title']

        body = request.form['body']

        title_err = ''

        body_err = ''



        if title == '':

            title_err = "Please enter a valid Title"

    

        if body == '':

            body_err = "Please enter a valid blog post"



    



        blog = Blog(title, body)

        db.session.add(blog)

        db.session.commit()



        return redirect('/blog')





    else:
        

        return render_template('newpost.html')       



        





if __name__ == '__main__':



    app.run()