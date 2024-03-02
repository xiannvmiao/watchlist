from watchlist import app, db
import click
from watchlist.models import User,Movie

# 自定义命令
@app.cli.command()
@click.option('--username', prompt=True, help='username used to login')
@click.option('--password', prompt=True, confirmation_prompt=True, hide_input=False,)
def admin(username,password):
    
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name = 'Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')







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