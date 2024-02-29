from flask import Flask,render_template,request,flash,redirect
from markupsafe import escape
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
import os
import sys
import click


WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
# 初始化扩展
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

# 自定义命令
@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
def forge():
    db.create_all()
    name = 'Mr huang'
    user = User(name=name)
    db.session.add(user)
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2015'},
    ]
    for m in movies:
        movie = Movie(title = m['title'], year = m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Done.')

# 上下文函数将每一个变量注入到所有模板中
@app.context_processor
def inject():
    user = User.query.first()
    return dict(user=user)

app.config['SECRET_KEY'] = 'SLDKFJLASKDFLA'

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        title = request.form.get("title")
        year = request.form.get("year")
        if not title or not year or len(year) != 4 or len(title) > 60:
            flash("Invaldi message")
            return redirect(url_for('index'))
        movie = Movie(title=title,year=year)
        db.session.add(movie)
        db.session.commit()
        flash("Item commit")
        return redirect(url_for("index"))

    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.route('/home/<name>')
def user_page(name):
    return f'User: {escape(name)}'

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page',name='JackMa'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for',num=5))
    return 'TestPage' 

@app.errorhandler(404)
def page_no_found(e):
    return render_template('404.html'),404

# 编辑页面
# 通过index页面拿到movie_id（模型类中设置的primary_key)
@app.route('/movie/edit<int:movie_id>',methods=['GET','POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid update')
            return redirect(url_for('edit',movie_id=movie_id))

        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item updated')
        return redirect(url_for('index'))
        
    return render_template('edit.html',movie=movie)

@app.route('/movie/delete/<int:movie_id>',methods='POST')
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    db.session.delete(movie)
    db.session.commit()
    flash("Item deleted")
    return redirect(url_for('index'))



