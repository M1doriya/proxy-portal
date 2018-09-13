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
from . import update


app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///C:/Users/DELL/new/DBMS-Project/dbms.db'
db = SQLAlchemy(app)

UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class input(db.Model):
	__tablename__ = 'input'
	column_display_pk = True
	curr_date = db.Column(db.DateTime(), primary_key=True)
	data = db.Column(db.String(40))
	


class MyInputView(ModelView):
	column_display_pk = True
	can_create = True
	column_list = ('curr_date', 'data')
	form_columns = ['curr_date', 'data']
	column_filters = ['curr_date', 'data']



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



current = None
type1 = ""


@app.route('/')
def index():
   return redirect(url_for('login'))

@app.route('/login',methods = ['GET','POST'])
def login():
	message = None
	global current,type1

	if request.method == 'GET':
		return render_template("login.html",message = None)
		
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
	return render_template("login.html",message = message)
    


if __name__ == '__main__':
	app.debug = True
	app.secret_key = os.urandom(12)

	db.create_all()

	app.run(debug = True)