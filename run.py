from flask import Flask
from flask.ext.login import LoginManager, login_required, login_user, logout_user
from flask_wtf import Form
from wtforms import StringField, DecimalField
from wtforms.validators import DataRequired
from flask import request, abort, redirect, url_for, render_template

app = Flask(__name__)

app.config['SECRET_KEY'] = 'very strong secret key'

login_manager = LoginManager()
login_manager.init_app(app)

class User:
    def __init__(self, id, passwd):
        self.id = id
        self.passwd = passwd

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return self.id


users = [
    User(id=0, passwd='0'),
    User(id=1, passwd='1'),
    User(id=2, passwd='2')
]

@login_manager.user_loader
def load_user(id):
    if id > len(users) - 1:
        return None
    return users[int(id)]

class MyForm(Form):
      user_id = DecimalField('user_id', validators=[DataRequired()])
      passwd = StringField('passwd', validators=[DataRequired()])

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = MyForm()
    if form.validate_on_submit():
        if form.passwd.data != users[int(form.user_id.data)].passwd:
            return render_template('login.html', form=form)

        login_user(users[int(form.user_id.data)])

        return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', form=form)

@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
