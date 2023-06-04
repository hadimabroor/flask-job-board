from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from .models import User
from . import db
from .functions import trim

auth = Blueprint("auth", __name__)

@auth.route('/signup')
def signup():
	return render_template('signup.html')

@auth.route('/signup', methods=["POST"])
def signup_post():
	name = request.form['name']
	username = request.form['username']
	email = request.form['email']
	password1 = request.form['password1']
	password2 = request.form['password2']

	user = User.query.filter_by(email=email).first()

	if user:
		flash('A user with this email already exists')
		return redirect(url_for('auth.signup'))
	elif password1 != password2:
		flash('Both passwords doesn\'t match')
		return redirect(url_for('auth.signup'))

	newUser = User(name=name, username=trim(username), email=email, password=generate_password_hash(password1), role="user")
	db.session.add(newUser)
	db.session.commit()

	return redirect(url_for('auth.login'))

@auth.route('/biz-signup')
def biz_signup():
	return render_template('biz-signup.html')

@auth.route('/biz-signup', methods=["POST"])
def biz_signup_post():
	name = request.form['name']
	username = request.form['company']
	email = request.form['email']
	password1 = request.form['password1']
	password2 = request.form['password2']

	user = User.query.filter_by(email=email).first()

	if user:
		flash('An employee with this email already exists')
		return redirect(url_for('auth.biz_signup'))
	elif password1 != password2:
		flash('Both passwords doesn\'t match')
		return redirect(url_for('auth.biz_signup'))

	newUser = User(name=name, username=trim(username), email=email, password=generate_password_hash(password1))
	db.session.add(newUser)
	db.session.commit()

	return redirect(url_for('auth.biz_login'))

@auth.route('/login')
def login():
	return render_template('login.html')

@auth.route('/login', methods=["POST"])
def login_post():
	email = request.form['email']
	password = request.form['password']

	user = User.query.filter_by(email=email).first()

	if not user or not check_password_hash(user.password, password):
		flash('please check your login details and try again')
		return redirect(url_for('auth.login'))

	login_user(user, remember=True)
	return redirect(url_for('views.profile'))
	
@auth.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('views.home'))