from flask import Flask
from markupsafe import escape
from flask import url_for

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Welcome to Mypage!'

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