import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'blog.db')
app.config['SQLALCHEMY_TRACT_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)
    
@app.route('/')
def index():
    posts = BlogPost.query.all()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = BlogPost.query.filter_by(id=post_id).one()
    posted_date = post.date_posted.strftime('%B %d, %Y')
    return render_template("post.html", post=post, posted_date=posted_date)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/add')
def add():
    return render_template("add.html")

@app.route('/add_post', methods=['POST'])
def add_post():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']
    
    post = BlogPost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())
    db.session.add(post)
    db.session.commit()
    # f"<h1>Title: {request.form['title']}, Subtitle: {request.form['subtitle']}, Author: {request.form['author']}, Content: {request.form['content']}</h1>"
    return redirect(url_for('index'))

if __name__ == ("__main__"):
    app.run(debug=True)