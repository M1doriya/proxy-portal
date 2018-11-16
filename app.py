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
	password = db.Column(db.String(50))
	name = db.Column(db.String(50))
	is_active = db.Column(db.Integer)
	image_link = db.Column(db.String(200))



class MyUserView(ModelView):
	column_display_pk = True
	can_create = True
	column_list = ('email','password','name','is_active','image_link')
	form_columns = ['email','password','name','is_active','image_link']
	column_filters = ['email','password','name','is_active','image_link']

class portInput(db.Model):
	__tablename__ = 'portInput'
	column_display_pk = True
	id = db.Column(db.String(200),primary_key=True)
	useremail = db.Column(db.String(40))
	port = db.Column(db.String(40))
	start_date = db.Column(db.DateTime())
	end_date = db.Column(db.DateTime())
	is_end = db.Column(db.Integer)
	is_fault = db.Column(db.Integer)


class MyPortInputView(ModelView):
	column_display_pk = True
	can_create = True
	column_list = ('id','useremail','port','start_date','end_date','is_end','is_fault')
	form_columns = ['id','useremail','port','start_date','end_date','is_end','is_fault']
	column_filters = ['id','useremail','port','start_date','end_date','is_end','is_fault']


class websiteInput(db.Model):
	__tablename__ = 'websiteInput'
	column_display_pk = True
	id = db.Column(db.String(200),primary_key=True)
	useremail = db.Column(db.String(40))
	website = db.Column(db.String(200))
	start_date = db.Column(db.DateTime())
	end_date = db.Column(db.DateTime())
	is_end = db.Column(db.Integer)
	is_fault = db.Column(db.Integer)


class MyWebsiteInputView(ModelView):
	column_display_pk = True
	can_create = True
	column_list = ('id','useremail','website','start_date','end_date','is_end','is_fault')
	form_columns = ['id','useremail','website','start_date','end_date','is_end','is_fault']
	column_filters = ['id','useremail','website','start_date','end_date','is_end','is_fault']



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

class HourlyAllData(db.Model):
	__tablename__ = 'HourlyAllData'
	column_display_pk = True
	id = db.Column(db.String(200),primary_key=True)
	hour = db.Column(db.Integer)
	curr_date = db.Column(db.DateTime())
	data_size = db.Column(db.Integer)

class MyHourlyAllDataView(ModelView):
	column_display_pk = True
	can_create = True
	column_list = ('id', 'hour','curr_date','data_size')
	form_columns = ['id', 'hour','curr_date','data_size']
	column_filters = ['id', 'hour','curr_date','data_size']



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
admin.add_view(MyPortInputView(portInput,db.session))
admin.add_view(MyWebsiteInputView(websiteInput,db.session))
admin.add_view(MyUserView(users,db.session))
admin.add_view(MyDeviceView(Device,db.session))
admin.add_view(MyDailyDataView(DailyData,db.session))
admin.add_view(MyHourlyAllDataView(HourlyAllData,db.session))


current = None
type1 = ""


@app.route('/')
def index():
	if session.get('logged_in'):
		return redirect('dashboard')
	else:
		return redirect('login')
	global current
	session['logged_in'] = True
	# making files like user_squid.conf and user_mac.txt
	name=current[:-12]       # eg. name = iit2016047
	conn = sqlite3.connect('students.sqlite3')
	cur = conn.cursor()
	cur.execute("SELECT * FROM users WHERE email = (?)",(current,))
	if not cur.fetchone(): 
		''''filename = "/etc/squid/users.conf"
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
		open(filename,"a").close()'''
		curr = conn.cursor()
		curr.execute("INSERT INTO users (email) VALUES (?)",(current,))
		conn.commit() 
	conn.close()
	return redirect('dashboard')

@app.route('/login',methods = ['GET','POST'])
def login():
	message = None
	global current
	if session.get('logged_in'):
		return redirect('dashboard')

	if request.method == 'GET':
		return render_template("login.html",message = None)
		
	if request.method == 'POST':
		username=request.form.get('username',)
		print(current)
		password=request.form.get('pass',)
		print (username)
		print (password)					#### change to host url 
		conn = sqlite3.connect('students.sqlite3')
		print ("Opened database successfully")
		curr = conn.cursor()
		#curr.execute("SELECT count(*) FROM users WHERE email = ?", (request.form.get('username',''),))
		curr.execute("SELECT count(*) FROM users WHERE email = (?)",(username,))
		data = curr.fetchone()[0]
		if data ==0:
			print('There is no user%s'%request.form.get('username'))
			message = "PLEASE REGISTER USER DOES NOT EXIST"
		else:
			print('Component %s found in %s row(s)'%(username,data))
			'''curr.execute("SELECT count(*) FROM users WHERE email = (?) and is_active = (?)",(username,1))
			check = curr.fetchone()[0]
			if check==0:
				return render_template("login.html",message = "Please verify your email first")'''

			curr.execute("SELECT count(*) FROM users WHERE email = (?) and password = (?) ",(username,password))
			check = curr.fetchall()[0]
			print("the value of ----- :",check[0])
			if check[0] != 0:
				message = "success"
				print ("success")
				user=username.split("@")[0]
				session['logged_in'] = True
				current=username
				return redirect('dashboard')
			else:
				return render_template("login.html",message = "INCORRECT PASSWORD")	
		conn.close()
	return render_template("login.html",message = message)
      


@app.route('/register',methods = ['GET','POST'])
def register():
	message = None
	if request.method == 'GET':
		return render_template("student_register.html", message = message)
	if request.method == 'POST':
		nm = request.form.get('name',)
		email = request.form.get('email',)
		password=request.form.get('pass',)
		passwordc=request.form.get('passc',)
		if email.split("@")[1] != "iiita.ac.in":
			message="invalid email"
			return render_template("student_register.html", message = message)
		if password != passwordc:
			print ("successf")
			message="password doesn't match"
			return render_template("student_register.html", message = message)
		if password == passwordc:
			print ("success")
			conn = sqlite3.connect('students.sqlite3')
			cur = conn.cursor()
			sub = email[:3].upper()
			user_type = None
			#secret = random.randint(1000324312,10000000000123)
			conn = sqlite3.connect('students.sqlite3')
			cur = conn.cursor()
			cur.execute("SELECT * FROM users WHERE email = (?)",(email,))
			name=email.split("@")[0]
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
				file1.write('\nhttp_access allow '+name+'_website '+name+'_mac')
				file1.write('\nacl '+name+'_website_deny dstdomain "/etc/squid/deny_website.lst"')	
				file1.write('\nhttp_access deny '+name+'_website_deny '+name+'_mac')
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
				cur = conn.cursor()
				cur.execute("INSERT INTO USERS (email,name,password,is_active) values (?,?,?,?)",\
					(email,nm,password,1))	
				conn.commit() 
				print ("insert into user success")
				return redirect(url_for('login'))
			else :
				message = "Email already exists."
			#msg = Message('Hello', sender = 'iit2016047@iiita.ac.in', recipients = [email])
			#msg.body = "Hello confirm your email " + "http://127.0.0.1:5000/emailverify/"+email.split("@")[0]+"/"+str(secret)
			#mail.send(msg)
			conn.close()
			
	return render_template("student_register.html", message = message) 	
 
'''@app.route('/login')
def login():
	if not session.get('logged_in'):
	    callback=url_for('authorized', _external=True)
	    return google.authorize(callback=callback)
	else:
		return redirect('dashboard')
 '''
 
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
		if inputtext:
			curr = conn.cursor()
			curr.execute("INSERT INTO portInput (id,useremail,port,start_date,is_end,is_fault) VALUES (?,?,?,?,?,?)",(str(date1)+current,current,inputtext,date1,0,0))
			conn.commit()
		if inputtext2:
			curr = conn.cursor()
			curr.execute("INSERT INTO websiteInput (id,useremail,website,start_date,is_end,is_fault) VALUES (?,?,?,?,?,?)",(str(date1)+current,current,inputtext2,date1,0,0))
			conn.commit() 
		conn.close()
		name=current[:-12]
		if inputtext2:
			update.add_website(name,inputtext2)
		if inputtext1:
			update.add_website(name,inputtext)
		
		#update.update_port(inputtext)
		message = "port/website request accepted"
		return redirect('dashboard')


@app.route('/addDevice',methods = ['GET','POST'])
def addDevice():
	message = None
	global current
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
		return redirect('dashboard')


@app.route('/dashboard',methods = ['GET'])
def dashboard():
	message = None
	global current
	print(current)
	if not session.get('logged_in'):
		return redirect('login')
	name=current[:-12]
	print(name)
	conn = sqlite3.connect('students.sqlite3')
	print ("Opened database successfully")
	curr = conn.cursor()
	curr.execute("SELECT mac_address,alias,id from Device where useremail=(?) ",(current,))
	data= curr.fetchall()
	curr.execute("SELECT port,start_date,id from portInput where useremail=(?) and is_end=(?)",(current,0,))
	active_ports = curr.fetchall()
	curr.execute("SELECT website,start_date,id from websiteInput where useremail=(?) and is_end=(?)",(current,0,))
	active_websites = curr.fetchall()
	curr.execute("SELECT port,start_date,id from portInput where useremail=(?) and is_end=(?)",(current,1,))
	past_ports = curr.fetchall()
	curr.execute("SELECT website,start_date,id from websiteInput where useremail=(?) and is_end=(?)",(current,1,))
	past_websites = curr.fetchall()
	conn.close()
	return render_template("dashboard.html",name = name,data=data,active_ports=active_ports,active_websites=active_websites,past_ports=past_ports,past_websites=past_websites)

@app.route('/removeMAC/<id>',methods = ['GET'])
def removeMAC(id):
	global current
	print(id)
	conn = sqlite3.connect('students.sqlite3')
	print ("Opened database successfully")
	curr = conn.cursor()
	curr.execute("DELETE from Device where id=(?) and useremail=(?) ",(id,current,))
	conn.commit()
	conn.close()
	return redirect('dashboard')

@app.route('/removePort/<id>',methods = ['GET'])
def removePort(id):
	global current
	print(id)
	date1 = datetime.now()
	conn = sqlite3.connect('students.sqlite3')
	print ("Opened database successfully")
	curr = conn.cursor()
	curr.execute("UPDATE portInput set is_end=(?),end_date=(?) where id=(?) and useremail=(?) ",(1,date1,id,current,))
	conn.commit()
	conn.close()
	return redirect('dashboard')

@app.route('/removeWebsite/<id>',methods = ['GET'])
def removeWebsite(id):
	global current
	print(id)
	date1 = datetime.now()
	conn = sqlite3.connect('students.sqlite3')
	print ("Opened database successfully")
	curr = conn.cursor()
	curr.execute("UPDATE websiteInput set is_end=(?),end_date=(?) where id=(?) and useremail=(?) ",(1,date1,id,current,))
	conn.commit()
	conn.close()
	return redirect('dashboard')
@app.route('/logout',methods = ['GET'])
def logout():
	current = ""
	session['logged_in'] = False
	return redirect('login')


if __name__ == '__main__':
	app.debug = True
	app.secret_key = os.urandom(12)

	db.create_all()

	app.run(debug = True,host="10.0.2.4",port=5000)
