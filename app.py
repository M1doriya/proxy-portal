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
import update


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
	is_active = db.Column(db.Integer)
	image_link = db.Column(db.String(200))



class MyUserView(ModelView):
	column_display_pk = True
	can_create = True
	column_list = ('email','username','name','is_active','image_link')
	form_columns = ['email','username','name','is_active','image_link']
	column_filters = ['email','username','name','is_active','image_link']

class Input(db.Model):
	__tablename__ = 'Input'
	column_display_pk = True
	id = db.Column(db.String(200),primary_key=True)
	useremail = db.Column(db.String(40))
	curr_date = db.Column(db.DateTime())
	port_requested = db.Column(db.String(40))
	website_requested = db.Column(db.String(200))



class MyInputView(ModelView):
	column_display_pk = True
	can_create = True
	column_list = ('id','curr_date', 'useremail','port_requested','website_requested')
	form_columns = ['id','curr_date', 'useremail','port_requested','website_requested']
	column_filters = ['id','curr_date', 'useremail','port_requested','website_requested']


class Device(db.Model):
	__tablename__ = 'Device'
	column_display_pk = True
	id = db.Column(db.String(200),primary_key=True)
	useremail = db.Column(db.String(40))
	curr_date = db.Column(db.DateTime())
	mac_address = db.Column(db.String(40))
	alias = db.Column(db.String(40))




class MyDeviceView(ModelView):
	column_display_pk = True
	can_create = True
	column_list = ('id','curr_date', 'useremail','mac_address','alias')
	form_columns = ['id','curr_date', 'useremail','mac_address','alias']
	column_filters = ['id','curr_date', 'useremail','mac_address','alias']


class DailyData(db.Model):
	__tablename__ = 'DailyData'
	column_display_pk = True
	id = db.Column(db.String(200),primary_key=True)
	useremail = db.Column(db.String(100))
	curr_date = db.Column(db.DateTime())
	data_size = db.Column(db.Integer)

class MyDailyDataView(ModelView):
	column_display_pk = True
	can_create = True
	column_list = ('id', 'useremail','curr_date','data_size')
	form_columns = ['id', 'useremail','curr_date','data_size']
	column_filters = ['id', 'useremail','curr_date','data_size']



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
admin.add_view(MyInputView(Input,db.session))
admin.add_view(MyUserView(users,db.session))
admin.add_view(MyDeviceView(Device,db.session))
admin.add_view(MyDailyDataView(DailyData,db.session))


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
	current = data.split("\n")[2].lstrip().lstrip('"email":').lstrip().rstrip().rstrip(',').lstrip('"').rstrip('"')

	# making files like user_squid.conf and user_mac.txt
	name=current[:-12]
	conn = sqlite3.connect('students.sqlite3')
	cur = conn.cursor()
	cur.execute("SELECT * FROM users WHERE email = (?)",(current,))
	if not cur.fetchone(): 
		filename = "/etc/squid/users.conf"
		os.makedirs(os.path.dirname(filename), exist_ok=True)
		file1 = open(filename,"a")
		file1.write("\ninclude /etc/squid/config_files/"+name+"/"+name+"_squid.conf")
		file1.close()
		filename = "/etc/squid/config_files/"+name+"/"+name+"_squid.conf"
		os.makedirs(os.path.dirname(filename), exist_ok=True)
		file1 = open(filename,"a")
		file1.write('\nacl '+name+'_mac arp "/etc/squid/config_files/'+name+'/'+name+'_mac.lst"')
		file1.write('\nacl '+name+'_website dstdomain "/etc/squid/config_files/'+name+'/'+name+'_website.lst"')	
		file1.write('\nhttp_access deny '+name+'_website '+name+'_mac')
		#file1.write('\nhttp_access deny '+name+'_mac')
		file1.close()			
		filename = "/etc/squid/config_files/"+name+"/"+name+"_mac.lst"
		os.makedirs(os.path.dirname(filename), exist_ok=True)
		open(filename,"a").close()
		filename = "/etc/squid/config_files/"+name+"/"+name+"_port.lst"
		os.makedirs(os.path.dirname(filename), exist_ok=True)
		open(filename,"a").close()
		filename = "/etc/squid/config_files/"+name+"/"+name+"_website.lst"
		os.makedirs(os.path.dirname(filename), exist_ok=True)
		open(filename,"a").close()
		curr = conn.cursor()
		curr.execute("INSERT INTO users (email) VALUES (?)",(current,))
		conn.commit() 
	conn.close()
	return redirect('Userrequest')
 	
 
@app.route('/login')
def login():
	if not session.get('logged_in'):
	    callback=url_for('authorized', _external=True)
	    return google.authorize(callback=callback)
	else:
		return redirect('Userrequest')
 
 
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



@app.route('/Userrequest',methods = ['GET','POST'])
def Userrequest():
	message = None
	global current,type1
	print(current)
	if not session.get('logged_in'):
		return redirect('login')

	if request.method == 'GET':
		return render_template("request.html",message = None)
		
	if request.method == 'POST':
		inputtext = request.form.get('inputtext',)
		inputtext2 = request.form.get('inputtext2',)
		conn = sqlite3.connect('students.sqlite3')
		'''cur = conn.cursor()
		cur.execute("SELECT mac_address FROM Device WHERE useremail = (?) and alias = (?)",(current,inputtext2,))
		mac_address = cur.fetchone()[0]
		print(mac_address)'''
		date1 = datetime.now()
		
		print ("Opened database successfully")
		curr = conn.cursor()
		curr.execute("INSERT INTO Input (id,useremail,curr_date,port_requested,website_requested) VALUES (?,?,?,?,?)",(str(date1)+current,current,date1,inputtext,inputtext2))
		conn.commit() 
		conn.close()
		name=current[:-12]
		if inputtext2:
			update.add_website(name,inputtext2)
		#update.update_port(inputtext)
		message = "port/website request accepted"
		return render_template("request.html",message = message)


@app.route('/addDevice',methods = ['GET','POST'])
def addDevice():
	message = None
	global current,type1
	print(current)
	if not session.get('logged_in'):
		return redirect('login')

	if request.method == 'GET':
		return render_template("addDevice.html",message = None)
		
	if request.method == 'POST':
		inputtext = request.form.get('inputtext',)
		alias = request.form.get('alias',)
		
		date1 = datetime.now()
		print (inputtext)
		print (date1)
		conn = sqlite3.connect('students.sqlite3')
		print ("Opened database successfully")
		curr = conn.cursor()
		curr.execute("INSERT INTO Device (id,useremail,curr_date,mac_address,alias) VALUES (?,?,?,?,?)",(str(date1)+current,current,date1,inputtext,alias))
		conn.commit() 
		conn.close()
		name=current[:-12]
		update.add_mac(name,inputtext)
		#update.update_port(inputtext)
		return render_template("addDevice.html",message = message)


if __name__ == '__main__':
	app.debug = False
	app.secret_key = os.urandom(12)

	db.create_all()

	app.run(debug = False)
