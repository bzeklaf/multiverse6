import os
from app import app, db, bcrypt
from app.models import User
from flask import Flask, flash, redirect, render_template, request, jsonify, request, url_for, redirect, session
import docx2txt
from flask_bootstrap import Bootstrap
from app.tryout import cw_processing, appoint_processing, regular
from app.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

Bootstrap(app)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("index.html")

#CW
@app.route("/cw", methods=['POST'])
@login_required
def cw():

    target = os.path.join(APP_ROOT, 'images/')
    destination=''

    if not os.path.isdir(target):
        os.mkdir(target)


    for file in request.files.getlist("file"):
        filename = file.filename
        destination = "/".join([target, filename])
        file.save(destination)
    
    if request.method == 'POST':
        print(file)
        text = docx2txt.process(destination).lower()
        
        result=[] 
        for r in cw_processing(text):
        	result.append(r)
        print(cw_processing)

        #regex
        #result_RE = []
        #for r in regular(text):
        	#result_RE.append(r)
        #print(result_RE)----> add result_RE to reneder tmplate 

    return render_template('results.html', text=text, display=False, result=result)

#APP
@app.route("/appoint", methods=['POST'])
@login_required
def appoint():

    target = os.path.join(APP_ROOT, 'images/')
    destination=''

    if not os.path.isdir(target):
        os.mkdir(target)


    for file in request.files.getlist("file1"):
        filename = file.filename
        destination = "/".join([target, filename])
        file.save(destination)
    
    if request.method == 'POST':
        print(file)
        text = docx2txt.process(destination).lower()
        
        result=[] 
        for r in appoint_processing(text):
        	result.append(r)
        print(appoint_processing)

        #regex
        #result_RE = []
        #for r in regular(text):
        #	result_RE.append(r)
        #print(result_RE) #add result_RE to reneder tmplate 

    return render_template('results.html', text=text, display=False, result=result)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstname=form.firstname.data, surname=form.surname.data, enterdate=form.enterdate.data, company=form.company.data, companytype=form.companytype.data, email=form.email.data, password=hashed_password, county=form.city.data, city=form.city.data, phonenumber=form.phonenumber.data )
        db.session.add(user)
        db.session.commit()
        #flash(f'Account created for {form.firstname.data}!', 'success')#success is bootstrap
        return redirect(url_for('login'))
    return render_template("register.html", title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful', 'danger')
    return render_template("login.html", title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/account")
@login_required
def account():
    return render_template("account.html", title='Account')

@app.route("/benefits")
def benefits():
    return render_template("index.html#benefits", title='Benefits')