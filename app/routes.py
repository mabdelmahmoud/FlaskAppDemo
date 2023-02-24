from app import app
from flask import render_template, flash, redirect
from flask import request
from flask import url_for
from flask import jsonify
from app.forms import LoginForm
import requests

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            credentials = {"username": form.username.data, "password": form.password.data}
            response = requests.post(url_for('loginAPI', _external=True), json=credentials)
            dict = response.json()
            if dict['Success']:
                flash('Welcome user {}({})! You opted for remember_me={}'.format(form.username.data, dict['uid'], form.remember_me.data))
                return redirect(url_for('index'))
            else:
                flash('Invalid credentials')
    else:
        if request.args:
            flash('GET method not allowed for login!')
        # else:
        #     flash('No data in request!')

    return render_template('login.html', title='Sign In', form=form)

@app.route('/index')
@app.route('/')
@app.route('/index3')
#a view function – route handler
def index():
    user = {'username': 'mabdelmahmoud'}
    classes = [ {'classInfo': {'code': 'CSC324', 'title': 'DevOps'}, 'instructor': 'Moustafa Abdelmahmoud'},
                {'classInfo': {'code': 'CSC184', 'title': 'Python Programming'}, 'instructor': 'Evan Noynaert'}]
    return render_template('index.html', title='Home', user=user, classes=classes)

@app.route('/json')
def jsonTest():
    instructor = {
        "username": "mabdelmahmoud",
        "role": "instructor",
        "uid": 11,
        "name": {
            "firstname": "moustafa",
            "lastname": "abdelmahmoud"
        }
    }
    return jsonify(instructor)

@app.route('/loginapi', methods=['GET', 'POST'])
@app.route('/restlogin', methods=['GET', 'POST'])
def loginAPI():
    json_data = request.get_json(force=True)
    if json_data:
        username = json_data["username"]
        password = json_data["password"]
    else:
        return '{"Success": false}'
    if username == 'mabdelmahmoud' and password == '123':
        return jsonify(Success=True, uid=11)
    return '{"Success": false}'
