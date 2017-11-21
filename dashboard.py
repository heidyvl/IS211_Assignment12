from flask import Flask, render_template, request, g, redirect, session, url_for, escape, abort, flash
import re
import sqlite3
from contextlib import closing

DATABASE = 'hw12.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'password'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('dashboard'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    cur = g.db.execute('select fname, lname from Students order by id desc')
    Students = [dict(fname=row[0], lname=row[1]) for row in cur.fetchall()]
    cur = g.db.execute('select subject, questions, date from Quizzes order by id desc')
    Quizzes = [dict(subject=row[0], questions=row[1], date=row[2]) for row in cur.fetchall()]
    return render_template('dashboard.html', Students=Students, Quizzes=Quizzes)

@app.route('/student/add', methods=['POST', 'GET'])
def add_student():
    if request.method == 'GET':
        return render_template('add_student.html')
    if request.method=='POST':
        first_name=request.form['fname']
        last_name=request.form['lname']
        query="INSERT INTO Students(fname,lname) VALUES(?,?)"
        g.db.execute(query,(first_name,last_name))
        g.db.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('dashboard'))

@app.route('/quiz/add', methods=['POST', 'GET'])
def add_quiz():
    if request.method == 'GET':
        return render_template('add_quiz.html')
    if request.method=='POST':
        subject=request.form['subject']
        questions=request.form['questions']
        date=request.form['date']
        query="INSERT INTO Quizzes(subject,questions,date) VALUES(?,?,?)"
        g.db.execute(query,(subject,questions,date))
        g.db.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('dashboard'))
    
# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


if __name__ == '__main__':
    app.run()
