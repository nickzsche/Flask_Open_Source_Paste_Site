# Python
from flask import Flask, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    time = db.Column(db.String(50), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        message = request.form.get('message')
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_post = Post(name=name, message=message, time=time)
        db.session.add(new_post)
        db.session.commit()

    search = request.args.get('search')
    order = request.args.get('order')

    query = Post.query

    if search:
        query = query.filter(Post.name.contains(search))

    if order == 'old':
        query = query.order_by(Post.time)
    else:
        query = query.order_by(Post.time.desc())

    posts = query.all()

    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)