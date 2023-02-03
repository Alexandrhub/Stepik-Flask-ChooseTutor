import os

from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField

SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


class OrderForm(FlaskForm):
    name = StringField('Имя')
    phone = StringField('Телефон')


@app.route('/form/', methods=["GET", "POST"])
def render_form():
    form = OrderForm()
    if request.method == 'POST':
        name = form.name.data
        phone = form.phone.data
        return render_template('save.html', name=name, phone=phone)
    else:
        return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(debug=True, port=8881)
