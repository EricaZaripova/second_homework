import datetime
import os
import sqlite3

from flask import Flask, render_template, url_for, request, flash, get_flashed_messages, g, abort, session
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import LoginManager
from flask_app.flask_databases import FlaskDataBase


DATABASE = 'flaskapp.db'
DEBUG = True
SECRET_KEY = 'gheghgj3qhgt4q$#^#$he'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flaskapp.db')))
# login_manager = LoginManager(app)
fdb = None


@app.before_request
def db_connect():
    global fdb
    fdb = FlaskDataBase(get_db())


def create_db():
    """Creates new database from sql file."""
    db = connect_db()
    with app.open_resource('db_schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def connect_db():
    """Returns connention to apps database."""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.route('/')
def index():
    return render_template(
        'index.html',
        menu_url=fdb.get_menu(),
        session_status=session_status_checking(),
    )


@app.route('/page2')
def second():
    return render_template(
        'second.html',
        phone='+79172345678',
        email='myemail@gmail.com',
        current_date=datetime.date.today().strftime('%d.%m.%Y'),
        menu_url=fdb.get_menu(),
        session_status = session_status_checking(),
    )


@app.route('/user')
def profile():
    return render_template('user.html', menu_url=fdb.get_menu(), session_status=session_status_checking(),)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html', menu_url=fdb.get_menu(), session_status=session_status_checking(),)
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in emails(fdb.get_users()):
            if check_password_hash(fdb.get_password_hash(email)[2], password):
                flash('Вход выполнен', category='success')
                session['user'] = True
                return render_template('user.html', menu_url=fdb.get_menu(), session_status=session_status_checking(),)
            else:
                flash('Неверные email или пароль', category='error')
        else:
            flash('Email не существует', category='error')
        return render_template('login.html', menu_url=fdb.get_menu(), session_status=session_status_checking(),)
    else:
        raise Exception(f'Method {request.method} not allowed')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template('index.html', menu_url=fdb.get_menu(), session_status=session_status_checking(),)


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html', menu_url=fdb.get_menu(), session_status=session_status_checking(),)
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if checking_data(email, password):
            password_hash = generate_password_hash(password)
            res = fdb.add_user(email, password_hash)
            if res:
                flash('Пользователь добавлен', category='success')
                session['user'] = True
                return render_template('user.html', menu_url=fdb.get_menu(), session_status=session_status_checking(),)
            else:
                flash('Ошибка добавления', category='error')
                return render_template('registration.html', menu_url=fdb.get_menu(), session_status=session_status_checking(),)
        else:
            return render_template('registration.html', menu_url=fdb.get_menu(), session_status=session_status_checking(),)
    else:
        raise Exception(f'Method {request.method} not allowed')


def checking_data(email, password):
    flag = True
    if (not email) or (not password):
        flash('Заполните все поля!', category='error')
        flag = False
    if '@' not in email or '.' not in email:
        flash('Некорректный email!', category='error')
        flag = False
    if email in emails(fdb.get_users()):
        flash('Email уже зарегистрирован!', category='error')
        flag = False
    if len(password) < 8:
        flash('Слишком короткий пароль!', category='error')
        flag = False
    return flag


def emails(emails):
    addresses = []
    for email in emails:
        addresses.append(email[1])
    return addresses


def session_status_checking():
    if 'user' in session:
        return True
    return False


@app.teardown_appcontext
def close_db(error):
    """Close database connection if it exists."""
    if hasattr(g, 'link_db'):
        g.link_db.close()


if __name__ == '__main__':
    app.run(debug=True)
