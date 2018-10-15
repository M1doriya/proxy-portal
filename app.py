from flask import Flask,render_template,redirect, url_for, request, session
import sqlite3
from datetime import datetime, date
from functools import wraps
from flask import Flask,render_template,redirect, url_for,request,session,flash
import os
import random
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 
from werkzeug import secure_filename
import json
from flask_oauth import OAuth
from requests_oauthlib import OAuth2Session


app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"
GOOGLE_CLIENT_ID = '380096036354-p766je2egc68kknfofn15jm2ovktfnc8.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'CDdsTHtPV7XAD4QTkBAMcspV'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///C:/Users/DELL/new/DBMS-Project/dbms.db'
REDIRECT_URI = '/oauth2callback'

db = SQLAlchemy(app)
oauth = OAuth()

google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)


class users(db.Model):
	__tablename__ = 'users'
	column_display_pk = True
	email = db.Column(db.String(40),primary_key=True)
	username = db.Column(db.String(40))
	name = db.Column(db.String(50))
	dob = db.Column(db.Date())
	password = db.Column(db.String(50))
	type1 = db.Column(db.String(20))
	semester = db.Column(db.Integer)
	department = db.Column(db.String(30))
	is_active = db.Column(db.Integer)
	secret_key = db.Column(db.Integer)
	image_link = db.Column(db.String(200))



class MyUserView(ModelView):
	column_display_pk = True
	can_create = True
	column_list = ('email','username','name','dob','password','type1','semester','department','is_active','secret_key','image_link')
	form_columns = ['email','username','name','dob','password','type1','semester','department','is_active','secret_key','image_link']
	column_filters = ['email','username','name','dob','password','type1','semester','department','is_active','secret_key','image_link']

class input(db.Model):
	__tablename__ = 'input'
	column_display_pk = True
	curr_date = db.Column(db.DateTime(), primary_key=True)
	username = db.Column(db.String(40))
	port_requested = db.Column(db.String(40))
	




class MyInputView(ModelView):
	column_display_pk = True
	can_create = True
	column_list = ('curr_date', 'username','port_requested')
	form_columns = ['curr_date', 'username','port_requested']
	column_filters = ['curr_date', 'username','port_requested']



adminlog = False
@app.route('/adminlogin', methods=['GET','POST'])
def adminlogin():
	print ("hi")
	global adminlog
	if request.method == 'GET':
		return render_template('adminlogin.html')
	if request.method == 'POST':
	    if request.form['password'] == 'password' and request.form['username'] == 'admin':
	        adminlog = True
	        #print "auth done.................................."
	        return redirect('http://127.0.0.1:5000/admin')				####change to host
	    else:
	        flash('wrong password!')
	

class MyAdminIndexView(AdminIndexView):
	def is_accessible(self):
		global adminlog
		if adminlog==False:
			return False
		if adminlog==True:
			adminlog=False
			return True


db.create_all()
admin = Admin(app,index_view=MyAdminIndexView())
admin.add_view(MyInputView(input,db.session))
admin.add_view(MyUserView(users,db.session))


current = None
type1 = ""


@app.route('/')
def index():
	global current
	access_token = session.get('access_token')
	if access_token is None:
		return redirect(url_for('login'))
 
	access_token = access_token[0]
	from urllib.request import Request, urlopen
	from urllib.error import URLError

	headers = {'Authorization': 'OAuth '+access_token}
	req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
	              None, headers)
	try:
		res = urlopen(req)
	except URLError as e:
	    if e.code == 401:
	        # Unauthorized - bad token
	        session.pop('access_token', None)
	        return redirect(url_for('login'))
	    return res.read()

	temp = res.read()
	data=temp.decode('utf8')
	#print(data.split("\n")[2].lstrip().lstrip('"email":').lstrip().rstrip().rstrip(','))
	session['logged_in'] = True
	current = data.split("\n")[2].lstrip().lstrip('"email":').lstrip().rstrip().rstrip(',')
	return redirect('portrequest')
 	
 
@app.route('/login')
def login():
	if not session.get('logged_in'):
	    callback=url_for('authorized', _external=True)
	    return google.authorize(callback=callback)
	else:
		return redirect('portrequest')
 
 
def get_google_auth(token=None):
    if token:
        return OAuth2Session(GOOGLE_CLIENT_ID, token=token)
    
    oauth = OAuth2Session(
        GOOGLE_CLIENT_ID,
        redirect_uri=REDIRECT_URI)

    return oauth

 
@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('index'))
 
 
@google.tokengetter
def get_access_token():
    return session.get('access_token')



@app.route('/portrequest',methods = ['GET','POST'])
def portrequest():
	message = None
	global current,type1
	print(current)
	if request.method == 'GET':
		return render_template("portrequest.html",message = None)
		
	if request.method == 'POST':
		inputtext = request.form.get('inputtext',)
		date1 = datetime.now()
		print (inputtext)
		print (date1)
		conn = sqlite3.connect('students.sqlite3')
		print ("Opened database successfully")
		curr = conn.cursor()
		curr.execute("INSERT INTO input (curr_date,data) VALUES (?,?)",(date1,inputtext))
		conn.commit() 
		conn.close()
		update.update_port(inputtext)
		return render_template("portrequest.html",message = message)


if __name__ == '__main__':
	app.debug = False
	app.secret_key = os.urandom(12)

	db.create_all()

	app.run(debug = False)
