from flask import Flask,render_template,redirect, url_for, request
import sqlite3
from datetime import datetime, date
from functools import wraps
from flask import Flask,render_template,redirect, url_for,request,session,flash
import os
import random
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 
from werkzeug import secure_filename
import json
#import tkMessageBox


app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///C:/Users/DELL/new/DBMS-Project/dbms.db'
db = SQLAlchemy(app)




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


'''conn = sqlite3.connect('students.sqlite3')
cur = conn.cursor()
cur.execute("DROP TABLE rating")


# #list_columns=['r_id','course_code','question_id','faculty_email','student_email','rating']



# @app.route('/new', methods = ['GET', 'POST'])
# def new():
#    if request.method == 'POST':
#       if not request.form['name'] or not request.form['city'] or not request.form['addr']:
#          flash('Please enter all the fields', 'error')
#       else:
#          student = students(request.form['name'], request.form['city'],
#             request.form['addr'], request.form['pin'])
         
#          db.session.add(student)
#          db.session.commit()
#          flash('Record was successfully added')
#          return redirect(url_for('show_all'))
#    return render_template('new.html')'''


# # app.config['MAIL_SERVER']='smtp.gmail.com'
# # app.config['MAIL_PORT'] = 587
# # app.config['MAIL_USERNAME'] = ''
# # app.config['MAIL_PASSWORD'] = ''
# # app.config['MAIL_USE_TLS'] = True
# # app.config['MAIL_USE_SSL'] = False

# # mail = Mail(app)


# #sqliteAdminBP = sqliteAdminBlueprint(dbPath = 'students.sqlite3')
# '''conn = sqlite3.connect('students.sqlite3')
# print ("Opened database successfully")
# sqliteAdminBP = sqliteAdminBlueprint(dbPath = 'students.sqlite3')
# #app.register_blueprint(sqliteAdminBP, url_prefix='/admin')
# conn.execute('CREATE TABLE IF NOT EXISTS courses (course_code TEXT primary key,couse_name TEXT, credits INT, department TEXT, semester INT)')
# print ("COURSES Table created successfully")
# conn.execute('CREATE TABLE IF NOT EXISTS users ( email TEXT primary key, username TEXT,name TEXT, dob DATE, pass TEXT, type TEXT, semester INT,department TEXT,is_active INT,secret_key INT)')
# print ("USERS Table created successfully")
# conn.execute('CREATE TABLE IF NOT EXISTS users_courses (S_no integer not null primary key AUTOINCREMENT,useremail TEXT,course_code TEXT, foreign key(useremail) references users(email),foreign key (course_code) references courses(course_code))')
# print ("USERS_courses Table created successfully")
# conn.execute('CREATE TABLE IF NOT EXISTS admin (username TEXT primary key, pass TEXT, email TEXT)')
# print ("ADMIN Table created successfully")
# conn.execute('CREATE TABLE IF NOT EXISTS query (S_no integer not null primary key AUTOINCREMENT,useremail TEXT,query TEXT,reply_to_query TEXT,seen integer,foreign key (useremail) references users(email))')
# print ("QUERY Table created successfully")
# conn.execute('CREATE TABLE IF NOT EXISTS questions (question_id TEXT primary key, question_type TEXT, question TEXT)')
# print ("QUESTIONS Table created successfully")
# conn.execute('CREATE TABLE IF NOT EXISTS question_answer (S_no integer not null primary key AUTOINCREMENT,question_id TEXT, useremail TEXT,foreign key (useremail) references users(email),foreign key (question_id) references questions(question_id))')
# print ("QUESTIONS Table created successfully")
# conn.execute('CREATE TABLE IF NOT EXISTS rating (r_id integer not null primary key AUTOINCREMENT,course_code TEXT, question_id TEXT, faculty_email TEXT,student_email TEXT,rating INT)')
# print ("RATING Table created successfully")
# cur = conn.cursor()
# cur.execute("SELECT * FROM users")
# al = cur.fetchall()
# print (al)
# cur.execute("SELECT * FROM query")
# al = cur.fetchall()
# print (al)
# conn.close()'''



'''
sqliteAdminBP = sq liteAdminBlueprint(
  dbPath = 'students.sqlite3',
  decorator = do_admin_login
)	
app.register_blueprint(sqliteAdminBP, url_prefix='/admin')'''
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
   return render_template("index.html")


@app.route('/login',methods = ['GET','POST'])
def login():
	message = None
	global current,type1
	if session.get('logged_in'):
		conn = sqlite3.connect('students.sqlite3')
		print ("Opened database successfully")
		curr = conn.cursor()
		curr.execute('SELECT type1 FROM users where email = (?)',(current+"@iiita.ac.in",))
		typeo = curr.fetchone()[0]
		if typeo=="Student":
			return redirect(url_for('dashboard',id = current))
		elif typeo=="Faculty":
			return redirect(url_for('facultydashboard',id = current))

	if request.method == 'GET':
		return render_template("login.html",message = None)
		
	if request.method == 'POST':
		username=request.form.get('username',)
		password=request.form.get('pass',)
		print (username)
		print (password)
		if password == 'password' and username == 'admin':
			session['admin_logged_in'] = True
			return redirect('http://127.0.0.1:5000/admin')						#### change to host url 
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
			curr.execute("SELECT count(*) FROM users WHERE email = (?)",(username,))
			check = curr.fetchone()[0]
			if check==0:
				return render_template("login.html",message = "account does not exist")

			curr.execute("SELECT count(*) FROM users WHERE email = (?) and password = (?)",(username,password))
			check = curr.fetchall()[0]
			print ("the value of ----- :"),check[0]
			if check[0] != 0:
				message = "success"
				print ("success")
				user=username.split("@")[0]
				session['logged_in'] = True
				current = user

				curr.execute("SELECT type1 FROM users WHERE email = (?)",(username,))
				user_type=curr.fetchone()[0]
				conn.close()
				return redirect(url_for('portrequest',id=user))
			else:
				return render_template("login.html",message = "INCORRECT PASSWORD")	
		conn.close()
	return render_template("login.html",message = message)

@app.route('/portrequest',methods = ['GET','POST'])
def portrequest():
	message = None
	global current,type1
	
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
	app.debug = True
	app.secret_key = os.urandom(12)

	db.create_all()

	app.run(debug = True)