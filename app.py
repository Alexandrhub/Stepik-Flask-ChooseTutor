import os
import json
from random import shuffle, randint

from flask import Flask, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy

SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    about = db.Column(db.String, unique=True, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    picture = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    goals = db.Column(db.String, nullable=False)
    free = db.Column(db.String)
    teacher_relations = db.relationship("Booking", back_populates="teacher_relation")


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    teacher_relation = db.relationship("Teacher", back_populates="teacher_relations")
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))


class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    goal = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)


db.create_all()

ru_days = {
    'mon': 'Понедельник',
    'tue': 'Вторник',
    'wed': 'Среда',
    'thu': 'Четверг',
    'fri': 'Пятница',
    'sat': 'Суббота',
    'sun': 'Воскресение'
}

date = {
    'teachers': db.session.query(Teacher).all(),
    'goals': json.loads(open('goals.json', 'r', encoding='utf-8').read())
}


@app.route('/')
def render_index():
    return render_template('index.html')


@app.route('/all')
def render_all():
    return render_template('all.html')


@app.route('/goals/<goal>/')
def render_goal(goal):
    return render_template('goal.html', goal=goal)


@app.route('/profiles/<id>')
def render_profile(id):
    return render_template('profile.html', id=id)


@app.route('/request')
def render_request():
    return render_template('request.html')


@app.route('/request_done')
def render_request_done():
    return render_template('request_done.html')


@app.route('/booking/<id>/<day>/<time>/')
def render_request_booking(id, day, time):
    return render_template('booking.html')


@app.route('/booking_done/')
def render_request_booking_done():
    return render_template('booking_done.html')


if __name__ == '__main__':
    app.run(debug=True, port=8881)
