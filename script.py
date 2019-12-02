# hello
from flask import Flask, session, render_template, request, redirect, g, url_for
from flask_mail import Mail, Message
import os
import sqlite3
import random
import string
import hashlib
import binascii
from urllib.parse import quote, unquote
from werkzeug import secure_filename
import shutil
from datetime import date, datetime

def hash_password(password, salt):
	pwdHash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
	pwdHash = str(binascii.hexlify(pwdHash))[2:-1]
	return pwdHash

def verify_password(storedHash, password, salt):
	pwdHash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt.encode('ascii'), 100000)
	pwdHash = str(binascii.hexlify(pwdHash))[2:-1]
	return pwdHash == storedHash

def encodeUrlText(text):
	return quote(quote(text, safe = ''))

def decodeUrlText(text):
	return unquote(unquote(text))


app = Flask(__name__)
# app.secret_key = os.urandom(24)
app.secret_key = "secret!!!"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'apartment.management.system.nitk@gmail.com'
app.config['MAIL_PASSWORD'] = 'ComputingLab'

mail = Mail(app)

@app.before_request
def before_request():
	g.user = None
	if 'user' in session:
		g.user = session['user']

@app.route("/")
def hello():
	return render_template('home.html')

@app.route("/logout")
def logout():
	return redirect(url_for('login'))

@app.route("/login", methods = ['GET', 'POST'])
def login():

	session.pop('user', None)

	if request.method == 'POST':
		session.pop('user', None)

		uid = request.form['userid']
		pwd = request.form['password']

		# print(uid, pwd)

		conn = sqlite3.connect('data/data.db')
		cursor = conn.execute("SELECT pwdHash, salt, userType, pwdCh FROM users WHERE user_id='"+uid+"'")

		cursor = cursor.fetchall()

		if len(cursor) != 0:
			storedHash = cursor[0][0]
			salt = cursor[0][1]
			if verify_password(storedHash, pwd, salt):
				session['user'] = uid
				if cursor[0][3] == 0:
					return redirect(url_for('chPwd'))
				elif cursor[0][2] == 0:
					return redirect(url_for('welcomeH'))
				else:
					return redirect(url_for('welcomeH'))#modified here


		return render_template('login.html', invalid = 'true')


	return render_template('login.html', invalid = 'false')

@app.route("/register")
def register():
	session.pop('user', None)
	return render_template('register.html')

@app.route("/President")
def President():
	return render_template('President.html')

@app.route("/Secretary")
def Secretary():
	return render_template('Secretary.html')

@app.route("/Treasurer")
def Treasurer():
	return render_template('Treasurer.html')

@app.route("/OfficeBearer")
def OfficeBearer():
	return render_template('OfficeBearer.html')


@app.route("/welcomeH")
def welcomeH():

	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))
	uid = decodeUrlText(uid)

	conn = sqlite3.connect('data/data.db')
	cursor = conn.execute("SELECT * FROM homeOwns WHERE aptNo='"+uid+"'")

	cursor = cursor.fetchall()

	userName = cursor[0][3]
	if userName == None or userName == "None":
		userName = ""

	userDoB = cursor[0][4]
	if userDoB == None or userDoB == "None":
		userDoB = ""

	userEmail = cursor[0][1]
	if userEmail == None or userEmail == "None":
		userEmail = ""

	userPhone = cursor[0][2]
	if userPhone == None or userPhone == "None":
		userPhone = ""

	cursor = conn.execute("SELECT tenant_id, name from apt_tenant NATURAL JOIN tenants WHERE aptNo='"+uid+"'")

	tenants = ""

	for row in cursor:
		tenants += "<a href='/tenant/"+str(row[0])+"'><button class='btn btn-info' style='margin: 5px'>"+row[1]+"</button></a><br>\n"

	# Finding user type for additonal responsibilty
	cursor = conn.execute("SELECT userType from users where user_id = '"+uid+"'" )
	cursor = cursor.fetchall()
	userType = cursor[0][0] # User type here

	if(userType==0):
		userTypeHTML =""

	elif(userType==1):
		userTypeHTML = "<a style=\"color:black;font-size:25px;text-decoration:none;\" href=\"President\">President</a>"

	elif(userType==2):
		userTypeHTML = "<a  style=\"color:black;font-size:25px;text-decoration:none;\" href=\"Secretary\" >Secretary</a>"

	elif(userType==3):
		userTypeHTML = "<a  style=\"color:black;font-size:25px;text-decoration:none;\" href=\"Treasurer\" >Treasurer</a>"

	elif(userType==4):
		userTypeHTML = "<a  style=\"color:black;font-size:25px;text-decoration:none;\" href=\"OfficeBearer\" >OfficeBearer</a>"
	else:
		pass



	return render_template('welcomeH.html', user = uid, userName = userName, userDoB = userDoB, userEmail = userEmail, userPhone = userPhone, tenants =tenants, userType=userTypeHTML)

@app.route("/welcomeM")
def welcomeM():

	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	return render_template('welcomeH.html', user = uid)

@app.route("/test")
def test():
	conn = sqlite3.connect('data/data.db')
	cursor = conn.execute("SELECT * FROM homeOwns")

	cursor = cursor.fetchall()

	res = ""
	for row in cursor:
		res += row[0]+","+row[1]+","+row[2]+","+row[3]+"\n"


	return res

@app.route("/checkAptNo/<aptNo>")
def checkAptNo(aptNo):

	aptNo = decodeUrlText(aptNo)

	conn = sqlite3.connect('data/data.db')
	cursor = conn.execute("SELECT registered FROM apartments WHERE aptNo='"+aptNo+"'")

	cursor = cursor.fetchall()

	if len(cursor) == 0:
		return "absent"
	elif cursor[0][0] != 0:
		return "exists"
	else:
		return "open"

@app.route("/registerUser/<uid>/<email>/<phone>")
def registerUser(uid, email, phone):

	uid = decodeUrlText(uid)
	email = decodeUrlText(email)
	phone = decodeUrlText(phone)

	stringLength = 15
	password_characters = string.ascii_letters + string.digits + "!#$%&'()*+,-./:;<=>?@[]^_`{|}~"#string.punctuation
	pwd = ''.join(random.choice(password_characters) for i in range(stringLength))

	conn = sqlite3.connect('data/data.db')

	salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
	pwdHash = hash_password(pwd, salt)


	try:


		msg = Message('Welcome to Apt Mgmt Sys',
			sender = 'apartment.management.system.nitk@gmail.com',
			recipients = [email])
		msg.body = 'Welcome to Apartment Management System!\n\n'
		# msg.body += 'Your one-time-password is:\t' + pwd + '\n\n'
		# msg.body += 'Kindly login to your account at the earliest. '
		msg.body += 'Please follow the below link to confirm your email before continuing to log in to your account:\n'
		msg.body += '127.0.0.1:5000/fLogin/' + encodeUrlText(uid) + "/" + encodeUrlText(pwd) + "\n\n"
		msg.body += 'Alternatively, you can also login using the one-time-password\t' + pwd + "\n\n"
		msg.body += 'Once you do this, you will be asked to create your own password which you will use henceforth.\n\n'
		msg.body += 'Thank you,\nApt Mgmt Sys\n\n\n'
		msg.body += 'Note: This is an auto-generated email. Please do not reply to it.'

		mail.send(msg)

		today = datetime.today()
		year = today.year
		month = today.month
		monthNum = (year - 1970) * 12 + month

		conn.execute("INSERT INTO homeOwns (aptNo, email, phone) VALUES ('"+uid+"', '"+email+"', '"+phone+"')")
		conn.execute("INSERT INTO users VALUES ('"+uid+"', '"+pwdHash+"', '"+str(salt)[2:-1]+"', 0, 0)")
		conn.execute("UPDATE apartments SET registered="+str(monthNum)+" WHERE aptNo='"+uid+"'")
		conn.execute("CREATE TABLE Maint_"+uid.replace("-", "_").replace("/", "_")+" (month INT, tran_num TEXT, amount REAL)")
		conn.commit()
		conn.close()

		os.mkdir("static/images/homeOwns/"+secure_filename(uid))

		return "success"

	except Exception as error:
		print(error)
		return error

# President Flat Owner Info
@app.route('/displayFlatOwner')
def displayFlatOwner():
	# print("Not functional")
	conn = sqlite3.connect('data/data.db')
	cur = conn.cursor()
	cur.execute("SELECT * from homeOwns;")
	data = cur.fetchall()
	return render_template('flatOwnerInfo.html', data=data)

@app.route('/approveProfile')
def approveProfile():
	conn = sqlite3.connect('data/data.db')
	cur = conn.cursor()
	# CHANGE WHERE APROVED IS 0
	cur.execute("SELECT * from apartments;")
	data = cur.fetchall()
	return render_template('approve.html', data=data)

@app.route('/approveUser2/<pre>/<post>')
def approveUser2(pre, post):
	conn = sqlite3.connect('data/data.db')
	cur = conn.cursor()
	id = pre+"/"+post
	cur.execute("UPDATE apartments SET approved='1' where aptNo='"+id+"' ; " )
	conn.commit()
	conn.close()
	return redirect(url_for('approveProfile'))

@app.route('/createProfile2')
def createProfile2():
	return render_template('newProfile.html')

@app.route('/Profile', methods=['POST'])
def Profile():
	conn = sqlite3.connect('data/data.db')
	cur = conn.cursor()
	apt1 = request.form['apt1']
	apt2 = request.form['apt2']
	apt3 = request.form['apt3']
	apt4 = request.form['apt4']
	apt5 = request.form['apt5']
	aptNo = apt1+"-"+apt2+"-"+apt3+"-"+apt4+"/"+apt5
	bedroom = request.form['bedroom']
	bathroom = request.form['bathroom']
	carp_area = request.form['carp_area']
	built_area = request.form['built_area']
	registered=0;
	conn.execute("INSERT INTO apartments (aptNo, registered, bedrooms, bathrooms, area, parking_area) VALUES ('"+aptNo+"', 0, '"+bedroom+"', '"+bathroom+"', '"+carp_area+"', '"+built_area+"')")
	conn.commit()
	conn.close()
	return redirect(url_for("approveProfile"))


# Secreatry Notice start
@app.route('/createNotice')
def createNotice():
	conn = sqlite3.connect('data/data.db')
	cur = conn.cursor()
	cur.execute("SELECT * from notice;")
	data = cur.fetchall()
	return render_template('createNotice.html', data=data)

@app.route('/recordNotice', methods=['POST'])
def recordNotice():
	print("Recieved")
	ref = request.form['ref_no']
	fromi = "Apartment Management"
	toi = request.form['to']
	title = request.form['title']
	body = request.form['body']
	do = str(date.today())
	conn = sqlite3.connect('data/data.db')
	conn.execute("INSERT INTO notice (ref_no, date, sender, receiver, title, body ) VALUES ('"+ref+"', '"+do+"', '"+fromi+"', '"+toi+"', '"+title+"', '"+body+"')")
	conn.commit()
	conn.close()

	return redirect(url_for("createNotice"))

@app.route('/deleteNotice/<id>')
def deleteNotice(id):
	conn = sqlite3.connect('data/data.db')
	print("QER")
	print(id)
	conn.execute("DELETE from notice where ref_no='"+id+"'  ")
	conn.commit()
	conn.close()
	return redirect(url_for("createNotice"))
# Secretary Notice end

# TREASUERER START

@app.route('/regularPayment')
def regularPayment():
	# conn = sqlite3.connect('data/data.db')
	# cur = conn.cursor()
	# cur.execute("SELECT * from electricity;")
	# row = cur.fetchone()
	# months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
	# today = datetime.today()
	# present = months[today.month]

	# if(row==None):
	# 	electricity = "You have not made any payment."
	# 	# electricity = cur.fetchall()
	# else:
	# 	monthname = months[(row[5]-1)%12]
	# 	electricity = "Last paid in the month of "+ str(monthname)+""

	# cur.execute("SELECT * from water;")
	# row = cur.fetchone()
	# if(row==None):
	# 	water = "You have not made any payment."
	# 	# electricity = cur.fetchall()
	# else:
	# 	# months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
	# 	monthname = months[(row[5]-1)%12]
	# 	water = "Last paid in the month of "+ str(monthname)+""

	# cur.execute("SELECT * from lift;")
	# row = cur.fetchone()
	# if(row==None):
	# 	lift = "You have not made any payment."
	# 	# electricity = cur.fetchall()
	# else:
	# 	issue = row[4]
	# 	newdate=str(int(issue[0:4])+1)+" "+issue[4:]
	# 	lift = "Valid upto "+newdate

	return render_template('regularPayment.html')#, electricity=electricity, water=water, present=present, lift=lift)

@app.route('/makeRegularPayment/<category>/<company>/<amount>')
def makeRegularPayment(category, company, amount):

	category = decodeUrlText(category)
	company = decodeUrlText(company)
	amount = decodeUrlText(amount)

	try:
		tranLength = 10
		tran_characters = string.ascii_letters + string.digits
		tranNum = ''.join(random.choice(tran_characters) for i in range(tranLength))

		today = datetime.today()
		year = today.year
		month = today.month
		monthNum = (year - 1970) * 12 + month

		conn = sqlite3.connect('data/data.db')
		conn.execute("INSERT INTO expense (category, company, tran_num, amount, month) VALUES ('"+category+"', '"+company+"', '"+tranNum+"', "+amount+", "+str(monthNum)+")")
		conn.commit()
		conn.close()

		return tranNum

	except Exception as e:
		print(e)
		return "failure"


# @app.route('/makeElectrictyPayment/<c_no>')
# def makeElectrictyPayment(c_no):
# 	conn = sqlite3.connect('data/data.db')
# 	cur = conn.cursor()
# 	c_no=str(c_no)
# 	today1 = str(date.today())
# 	today = datetime.today()
# 	year = today.year
# 	month = today.month
# 	monthNum = str((year - 1970) * 12 + month)
# 	cur.execute("INSERT INTO electricity (c_no, c_date, month, amount) VALUES ('"+c_no+"', '"+today1+"', '"+monthNum+"', '"+str(10000)+"' ) ");
# 	conn.commit()
# 	conn.close()
# 	return redirect(url_for("regularPayment"))

# @app.route('/makeWaterPayment/<c_no>')
# def makeWaterPayment(c_no):
# 	conn = sqlite3.connect('data/data.db')
# 	cur = conn.cursor()
# 	c_no=str(c_no)
# 	today1 = str(date.today())
# 	today = datetime.today()
# 	year = today.year
# 	month = today.month
# 	monthNum = str((year - 1970) * 12 + month)
# 	cur.execute("INSERT INTO water (c_no, c_date, month, amount) VALUES ('"+c_no+"', '"+today1+"', '"+monthNum+"', '"+str(10000)+"' ) ");
# 	conn.commit()
# 	conn.close()
# 	return redirect(url_for("regularPayment"))

# @app.route('/makeLiftPayment/<c_no>/<company>/<duration>')
# def makeLiftPayment(c_no, company, duration):
# 	conn = sqlite3.connect('data/data.db')
# 	cur = conn.cursor()
# 	c_no=str(c_no)
# 	today1 = str(date.today())
# 	today = datetime.today()
# 	year = today.year
# 	month = today.month
# 	monthNum = str((year - 1970) * 12 + month)
# 	cur.execute("INSERT INTO lift (company, c_no, date, duration, amount) VALUES ( '"+company+"'  ,'"+c_no+"', '"+today1+"', '"+duration+"', '"+str(50000)+"' ) ");
# 	conn.commit()
# 	conn.close()
# 	return redirect(url_for("regularPayment"))

# @app.route('/payment')
# def payment():
# 	if 'user' in session:
# 		uid = session['user']
# 	else:
# 		return redirect(url_for('login'))
#
# 	today = datetime.today()
# 	year = today.year
# 	month = today.month
# 	monthNum = (year - 1970) * 12 + month
#
# 	conn = sqlite3.connect('data/data.db')
#
# 	cursor = conn.execute("SELECT * FROM apartments WHERE aptNo='"+uid+"'")
#
# 	cursor = cursor.fetchall()
#
# 	regMonth = cursor[0][1]
#
# 	maintAmt = cursor[0][5] * 5 + cursor[0][6] * 100
#
# 	cursor = conn.execute("SELECT * FROM Maint_"+uid.replace("-", "_").replace("/", "_"))
#
# 	cursor = cursor.fetchall()
#
# 	if len(cursor) != 0:
# 		lastMonth = cursor[-1][0]
# 	else:
# 		lastMonth = regMonth - 1
#
# 	toPay = monthNum - lastMonth
#
# 	if toPay > 0:
# 		payDet = "You need to <strong>pay</strong> maintenance for <strong>" + str(toPay) + " months</strong>."
# 	elif toPay == 0:
# 		payDet = "Your maintenance payment is <strong>settled up!</strong>"
# 	else:
# 		payDet = "You have paid maintenance for <strong>" + str(-1 * toPay) + " months</strong> in <strong>advance</strong>."
#
# 	return render_template('payment.html', user = uid, payDet = payDet, maintAmt = maintAmt)


# TREASURER END


#User Notice Display
@app.route('/showNotice')
def showNotice():
	conn = sqlite3.connect('data/data.db')
	cur = conn.cursor()
	cur.execute("SELECT * from notice where approved='1';")
	data = cur.fetchall()
	return render_template("showNotice.html", data=data)

# President approve Notices
@app.route('/approveNotice')
def approveNotice():
	conn = sqlite3.connect('data/data.db')
	cur = conn.cursor()
	cur.execute("SELECT * from notice;")
	data = cur.fetchall()
	return render_template("approveNotice.html", data=data)

@app.route('/approveRecord/<id>')
def approveRecord(id):
	conn = sqlite3.connect('data/data.db')
	cur = conn.cursor()
	cur.execute("UPDATE notice SET approved='1' where ref_no='"+id+"'")
	conn.commit()
	conn.close()
	print(id)
	return redirect(url_for("approveNotice"))


# Treasure Expense Record
@app.route('/showExpenseForm')
def showExpenseForm():
	return render_template("treasurer_expense.html")

@app.route('/makeRecord', methods=['POST'])
def makeRecord():
	name = request.form['name']
	amount = request.form['amount']
	typer = request.form['category']
	conn = sqlite3.connect('data/data.db')
	do = str(date.today())
	conn.execute("INSERT INTO expense (name, amount, type, date ) VALUES ('"+name+"', '"+amount+"', '"+typer+"', '"+do+"')")
	conn.commit()
	conn.close()
	return redirect(url_for("showExpenseForm"))

@app.route("/complaint_page/")
def complaint_page():
	# Display user complaints with create option
	uid = session['user']
	conn = sqlite3.connect('data/data.db')
	cur = conn.cursor()
	cur.execute("SELECT * from complaint where user_id='"+uid+"' ")
	data = cur.fetchall()
	return render_template("complaint.html", data=data)

@app.route("/deleteComplaint/<id>")
def deleteComplaint(id):
	print("THis")
	conn = sqlite3.connect('data/data.db')
	cursor = conn.cursor()
	cursor.execute("DELETE FROM complaint where id='"+id+"' ")
	conn.commit()
	conn.close()

	return redirect(url_for("complaint_page"))

@app.route("/complaint",methods=['POST'])
def complaint():
	subject = request.form['subject']
	category = request.form['category']
	uid = session['user']
	conn = sqlite3.connect('data/data.db')
	do = str(date.today())
	conn.execute("INSERT INTO complaint (user_id, category, content, date) VALUES ('"+uid+"', '"+ category+"', '"+ subject+"', '"+do+"')")
	conn.commit()
	conn.close()

	return redirect(url_for("complaint_page"))

@app.route('/secretaryViewComplaint')
def secretaryViewComplaint():
	conn = sqlite3.connect('data/data.db')
	cursor = conn.cursor()
	cursor.execute("Select * from complaint")
	rows = cursor.fetchall();
	return render_template('secretaryViewComplaint.html', rows=rows)

@app.route('/viewComplaint')
def viewComplaint():
	conn = sqlite3.connect('data/data.db')
	cursor = conn.cursor()
	cursor.execute("Select * from complaint")
	rows = cursor.fetchall();
	return render_template('viewComplaint.html', rows=rows)

@app.route('/updateComplaintStatus/<id>')
def updateComplaintStatus(id):
	conn = sqlite3.connect('data/data.db')
	cursor = conn.cursor()
	cursor.execute("UPDATE complaint set status='Resolved' where id='"+id+"' ")
	conn.commit()
	conn.close()

	return redirect(url_for("secretaryViewComplaint"))

@app.route('/updateComplaintStatus2/<id>')
def updateComplaintStatus2(id):
	conn = sqlite3.connect('data/data.db')
	cursor = conn.cursor()
	cursor.execute("UPDATE complaint set status='Denied' where id='"+id+"' ")
	conn.commit()
	conn.close()

@app.route('/duespayment')
def duespayment():
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))


	today = datetime.today()
	year = today.year
	month = today.month
	monthNum = (year - 1970) * 12 + month
	
	months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
	conn = sqlite3.connect('data/data.db')
	auid = str(uid)
	tuid = auid.replace('/', '_')
	yuid = tuid.replace('-', '_')
	wuid = "Maint_" + yuid
	# print(wuid)

	cursor = conn.execute("SELECT * FROM "+wuid+"  ")
	cursor = cursor.fetchall()

	if len(cursor) != 0:
		lastMonth = cursor[-1][0]
	else:
		lastMonth = regMonth - 1

	toPay = monthNum - lastMonth

	income = "<table width='300px' cellpadding='5'>\n<tr>\n<th><center>Month</center></th>\n<th><center>Transaction Id</center></th>\n</tr>\n"
	incTot = 0

	for row in cursor:
		y = row[0] // 12 + 1970
		m = row[0] % 12
		if m == 0:
			m = 12
			y -= 1
		income += "<tr>\n<td><center>"+str(months[m-1])+"</center></td>\n<td><center>&#8377; "+str(row[1])+"</center></td>\n</tr>\n"

	income += "</table>"

	# if len(cursor) != 0:
	# 	lastMonth = cursor[-1][0]
	# else:
	# 	lastMonth = regMonth - 1
	#
	# toPay = monthNum - lastMonth

	if toPay > 0:
		payDet = "You need to <strong>pay</strong> maintenance for <strong>" + str(toPay) + " months</strong>."
	elif toPay == 0:
		payDet = "Your maintenance payment is <strong>settled up!</strong>"
	else:
		payDet = "You have paid maintenance for <strong>" + str(-1 * toPay) + " months</strong> in <strong>advance</strong>."

	return render_template('duespayment.html', income=income, payDet = payDet)

@app.route('/payment')
def payment():
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	today = datetime.today()
	year = today.year
	month = today.month
	monthNum = (year - 1970) * 12 + month

	conn = sqlite3.connect('data/data.db')

	cursor = conn.execute("SELECT * FROM apartments WHERE aptNo='"+uid+"'")

	cursor = cursor.fetchall()

	regMonth = cursor[0][1]

	maintAmt = cursor[0][5] * 5 + cursor[0][6] * 100

	cursor = conn.execute("SELECT * FROM Maint_"+uid.replace("-", "_").replace("/", "_"))

	cursor = cursor.fetchall()

	if len(cursor) != 0:
		lastMonth = cursor[-1][0]
	else:
		lastMonth = regMonth - 1

	toPay = monthNum - lastMonth

	if toPay > 0:
		payDet = "You need to <strong>pay</strong> maintenance for <strong>" + str(toPay) + " months</strong>."
	elif toPay == 0:
		payDet = "Your maintenance payment is <strong>settled up!</strong>"
	else:
		payDet = "You have paid maintenance for <strong>" + str(-1 * toPay) + " months</strong> in <strong>advance</strong>."

	return render_template('payment.html', user = uid, payDet = payDet, maintAmt = maintAmt)

@app.route('/makePayment/<months>')
def makePayment(months):

	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	months = int(months)

	try:
		conn = sqlite3.connect('data/data.db')

		cursor = conn.execute("SELECT * FROM apartments WHERE aptNo='"+uid+"'")

		cursor = cursor.fetchall()

		regMonth = cursor[0][1]

		maintAmt = cursor[0][5] * 5 + cursor[0][6] * 100

		cursor = conn.execute("SELECT * FROM Maint_"+uid.replace("-", "_").replace("/", "_"))

		cursor = cursor.fetchall()

		if len(cursor) != 0:
			lastMonth = cursor[-1][0]
		else:
			lastMonth = regMonth - 1

		tranLength = 10
		tran_characters = string.ascii_letters + string.digits
		tranNum = ''.join(random.choice(tran_characters) for i in range(tranLength))

		totPayment = months * maintAmt

		today = datetime.today()
		year = today.year
		month = today.month
		monthNum = (year - 1970) * 12 + month

		for i in range(months):
			lastMonth += 1

			conn.execute("INSERT INTO Maint_"+uid.replace("-", "_").replace("/", "_") + " VALUES ("+str(lastMonth)+", '"+tranNum+"', "+str(maintAmt)+")")
			conn.execute("INSERT INTO income (type, amount, user, month) VALUES ('Maintenance', " + str(totPayment) + ", '" + uid + "', " + str(monthNum) + ")")

		conn.commit()
		conn.close()

		return tranNum

	except Exception as e:

		print(e)

		return "failure"


@app.route("/fLogin/<uid>/<pwd>")
def fLogin(uid, pwd):

	uid = decodeUrlText(uid)
	pwd = decodeUrlText(pwd)

	print(uid)
	print(pwd)

	conn = sqlite3.connect('data/data.db')
	cursor = conn.execute("SELECT pwdHash, salt, userType, pwdCh FROM users WHERE user_id='"+uid+"'")

	cursor = cursor.fetchall()

	if len(cursor) != 0:
		storedHash = cursor[0][0]
		salt = cursor[0][1]
		if verify_password(storedHash, pwd, salt):
			session['user'] = uid
			if cursor[0][3] == 0:
				return redirect(url_for('chPwd'))

	return redirect(url_for('login'))

@app.route("/chPwd")
def chPwd():
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	return render_template('chPwd.html', user = uid)

@app.route("/chNewPwd/<pwd>")
def chNewPwd(pwd):
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	pwd = decodeUrlText(pwd)

	conn = sqlite3.connect('data/data.db')

	salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
	pwdHash = hash_password(pwd, salt)

	try:
		conn.execute("UPDATE users SET pwdHash='"+pwdHash+"', salt='"+str(salt)[2:-1]+"', pwdCh=1 WHERE user_id='"+uid+"'")
		conn.commit()
		conn.close()

		return "success"


	except sqlite3.Error as error:
		return error.message


@app.route("/updateUser/<phone>/<name>/<dob>")
def updateUser(phone, name, dob):
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	phone = decodeUrlText(phone)
	name = decodeUrlText(name)
	dob = decodeUrlText(dob)

	conn = sqlite3.connect('data/data.db')

	try:
		conn.execute("UPDATE homeOwns SET phone='"+phone+"', usrName='"+name+"', dob='"+dob+"' WHERE aptNo='"+uid+"'")
		conn.commit()
		conn.close()

		return "success"

	except sqlite3.Error as error:
		return error.message


@app.route('/tenant/<tid>')
def tenant(tid):

	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	conn = sqlite3.connect('data/data.db')

	cursor = conn.execute("SELECT * FROM apt_tenant WHERE aptNo='"+uid+"' AND tenant_id="+tid)

	cursor = cursor.fetchall()

	if len(cursor) == 0:
		return redirect(url_for('login'))

	cursor = conn.execute("SELECT * FROM tenants WHERE tenant_id="+tid)

	cursor = cursor.fetchall()

	name = cursor[0][1]
	email = cursor[0][7]
	mobile = cursor[0][6]
	dob = cursor[0][5]
	father = cursor[0][2]
	mother = cursor[0][3]
	occupation = cursor[0][4]
	address = cursor[0][8]
	photo = cursor[0][10]
	if photo == None:
		photo = "/static/images/user_def.png"
	idProof = cursor[0][11]
	if idProof == None:
		idProof = "No file uploaded yet!"
	else:
		idProof = '<img src="'+idProof+'" width = 400px>'
	addProof = cursor[0][12]
	if addProof == None:
		addProof = "No file uploaded yet!"
	else:
		addProof = '<img src="'+addProof+'" width = 400px>'


	return render_template('tenant.html', uid = uid, tid = tid, name = name, email = email, mobile = mobile, dob = dob, father = father,
		mother = mother, occupation = occupation, address = address, photo = photo, idProof = idProof, addProof = addProof)

@app.route('/editTenantName/<tid>/<name>')
def editTenantName(tid, name):
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	conn = sqlite3.connect('data/data.db')

	cursor = conn.execute("SELECT * FROM apt_tenant WHERE aptNo='"+uid+"' AND tenant_id="+tid)

	cursor = cursor.fetchall()

	if len(cursor) == 0:
		return redirect(url_for('login'))

	name = decodeUrlText(name)

	conn.execute("UPDATE tenants SET name='"+name+"' WHERE tenant_id="+tid)
	conn.commit()
	conn.close()

	return "success"

@app.route('/editTenantEmail/<tid>/<email>')
def editTenantEmail(tid, email):
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	conn = sqlite3.connect('data/data.db')

	cursor = conn.execute("SELECT * FROM apt_tenant WHERE aptNo='"+uid+"' AND tenant_id="+tid)

	cursor = cursor.fetchall()

	if len(cursor) == 0:
		return redirect(url_for('login'))

	email = decodeUrlText(email)

	conn.execute("UPDATE tenants SET email='"+email+"' WHERE tenant_id="+tid)
	conn.commit()
	conn.close()

	return "success"

@app.route('/editTenantMobile/<tid>/<mobile>')
def editTenantMobile(tid, mobile):
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	conn = sqlite3.connect('data/data.db')

	cursor = conn.execute("SELECT * FROM apt_tenant WHERE aptNo='"+uid+"' AND tenant_id="+tid)

	cursor = cursor.fetchall()

	if len(cursor) == 0:
		return redirect(url_for('login'))

	mobile = decodeUrlText(mobile)

	conn.execute("UPDATE tenants SET mobile='"+mobile+"' WHERE tenant_id="+tid)
	conn.commit()
	conn.close()

	return "success"

@app.route('/editTenantDob/<tid>/<dob>')
def editTenantDob(tid, dob):
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	conn = sqlite3.connect('data/data.db')

	cursor = conn.execute("SELECT * FROM apt_tenant WHERE aptNo='"+uid+"' AND tenant_id="+tid)

	cursor = cursor.fetchall()

	if len(cursor) == 0:
		return redirect(url_for('login'))

	dob = decodeUrlText(dob)

	conn.execute("UPDATE tenants SET dob='"+dob+"' WHERE tenant_id="+tid)
	conn.commit()
	conn.close()

	return "success"

@app.route('/editTenantFather/<tid>/<father>')
def editTenantFather(tid, father):
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	conn = sqlite3.connect('data/data.db')

	cursor = conn.execute("SELECT * FROM apt_tenant WHERE aptNo='"+uid+"' AND tenant_id="+tid)

	cursor = cursor.fetchall()

	if len(cursor) == 0:
		return redirect(url_for('login'))

	father = decodeUrlText(father)

	conn.execute("UPDATE tenants SET father='"+father+"' WHERE tenant_id="+tid)
	conn.commit()
	conn.close()

	return "success"

@app.route('/editTenantMother/<tid>/<mother>')
def editTenantMother(tid, mother):
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	conn = sqlite3.connect('data/data.db')

	cursor = conn.execute("SELECT * FROM apt_tenant WHERE aptNo='"+uid+"' AND tenant_id="+tid)

	cursor = cursor.fetchall()

	if len(cursor) == 0:
		return redirect(url_for('login'))

	mother = decodeUrlText(mother)

	conn.execute("UPDATE tenants SET mother='"+mother+"' WHERE tenant_id="+tid)
	conn.commit()
	conn.close()

	return "success"

@app.route('/editTenantOccup/<tid>/<occup>')
def editTenantOccup(tid, occup):
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	conn = sqlite3.connect('data/data.db')

	cursor = conn.execute("SELECT * FROM apt_tenant WHERE aptNo='"+uid+"' AND tenant_id="+tid)

	cursor = cursor.fetchall()

	if len(cursor) == 0:
		return redirect(url_for('login'))

	occup = decodeUrlText(occup)

	conn.execute("UPDATE tenants SET occupation='"+occup+"' WHERE tenant_id="+tid)
	conn.commit()
	conn.close()

	return "success"

@app.route('/editTenantAddr/<tid>/<addr>')
def editTenantAddr(tid, addr):
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	conn = sqlite3.connect('data/data.db')

	cursor = conn.execute("SELECT * FROM apt_tenant WHERE aptNo='"+uid+"' AND tenant_id="+tid)

	cursor = cursor.fetchall()

	if len(cursor) == 0:
		return redirect(url_for('login'))

	addr = decodeUrlText(addr)

	conn.execute("UPDATE tenants SET address='"+addr+"' WHERE tenant_id="+tid)
	conn.commit()
	conn.close()

	return "success"

@app.route('/editTenantPhoto/<tid>', methods = ['GET', 'POST'])
def editTenantPhoto(tid):
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	conn = sqlite3.connect('data/data.db')

	cursor = conn.execute("SELECT * FROM apt_tenant WHERE aptNo='"+uid+"' AND tenant_id="+tid)

	cursor = cursor.fetchall()

	if len(cursor) == 0:
		return redirect(url_for('login'))

	if request.method == 'POST':
		photo = request.files['photoFile']

		i = 0
		while (True):
			fname = "static/images/tenants/"+tid+"/photo"+str(i)+"." + photo.filename.split('.')[-1]
			if not os.path.exists(fname):
				break
			i += 1

		photo.save(fname)

		conn = sqlite3.connect('data/data.db')

		conn.execute("UPDATE tenants SET photo='/"+fname+"' WHERE tenant_id="+tid)
		conn.commit()
		conn.close()

		return redirect(url_for("tenant", tid = tid))

	return "oops"

@app.route('/uploadTenantIdProof/<tid>', methods = ['GET', 'POST'])
def uploadTenantIdProof(tid):
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	conn = sqlite3.connect('data/data.db')

	cursor = conn.execute("SELECT * FROM apt_tenant WHERE aptNo='"+uid+"' AND tenant_id="+tid)

	cursor = cursor.fetchall()

	if len(cursor) == 0:
		return redirect(url_for('login'))

	if request.method == 'POST':
		photo = request.files['photoFile']

		i = 0
		while (True):
			fname = "static/images/tenants/"+tid+"/idProof"+str(i)+"." + photo.filename.split('.')[-1]
			if not os.path.exists(fname):
				break
			i += 1

		photo.save(fname)

		conn = sqlite3.connect('data/data.db')

		conn.execute("UPDATE tenants SET id_proof='/"+fname+"' WHERE tenant_id="+tid)
		conn.commit()
		conn.close()

		return redirect(url_for("tenant", tid = tid))

	return "oops"

@app.route('/uploadTenantAddrProof/<tid>', methods = ['GET', 'POST'])
def uploadTenantAddrProof(tid):
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	conn = sqlite3.connect('data/data.db')

	cursor = conn.execute("SELECT * FROM apt_tenant WHERE aptNo='"+uid+"' AND tenant_id="+tid)

	cursor = cursor.fetchall()

	if len(cursor) == 0:
		return redirect(url_for('login'))

	if request.method == 'POST':
		photo = request.files['photoFile']

		i = 0
		while (True):
			fname = "static/images/tenants/"+tid+"/addProof"+str(i)+"." + photo.filename.split('.')[-1]
			if not os.path.exists(fname):
				break
			i += 1

		photo.save(fname)

		conn = sqlite3.connect('data/data.db')

		conn.execute("UPDATE tenants SET add_proof='/"+fname+"' WHERE tenant_id="+tid)
		conn.commit()
		conn.close()

		return redirect(url_for("tenant", tid = tid))

	return "oops"

@app.route('/homeOwner')
def homeOwner():
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	conn = sqlite3.connect('data/data.db')

	cursor = conn.execute("SELECT * FROM homeOwns WHERE aptNo='"+uid+"'")

	cursor = cursor.fetchall()

	flatNo = cursor[0][16]
	name = cursor[0][3]
	email = cursor[0][1]
	mobile = cursor[0][2]
	dob = cursor[0][4]
	father = cursor[0][7]
	mother = cursor[0][8]
	occupation = cursor[0][11]
	comm_address = cursor[0][9]
	perm_address = cursor[0][10]
	if cursor[0][12] == 1:
		occupancy = "checked"
	else:
		occupancy = ""
	photo = cursor[0][5]
	if photo == None:
		photo = "/static/images/user_def.png"

	idProof = cursor[0][6]
	if idProof == None:
		idProof = "No file uploaded yet!"
	else:
		idProof = '<img src="'+idProof+'" width = 400px>'
	commAddProof = cursor[0][13]
	if commAddProof == None:
		commAddProof = "No file uploaded yet!"
	else:
		commAddProof = '<img src="'+commAddProof+'" width = 400px>'
	permAddProof = cursor[0][14]
	if permAddProof == None:
		permAddProof = "No file uploaded yet!"
	else:
		permAddProof = '<img src="'+permAddProof+'" width = 400px>'
	saleDeed = cursor[0][15]
	if saleDeed == None:
		saleDeed = "No file uploaded yet!"
	else:
		saleDeed = '<img src="'+saleDeed+'" width = 400px>'

	return render_template('homeOwnerDet.html', uid = uid, name = name, email = email, mobile = mobile, dob = dob, father = father,
		mother = mother, occupation = occupation, comm_address = comm_address, perm_address = perm_address, photo = photo,
		occupancy = occupancy, idProof = idProof, commAddProof = commAddProof, permAddProof = permAddProof,
		saleDeed = saleDeed, flatNo = flatNo)

@app.route('/editHomeOwnFlat/<flat>')
def editHomeOwnFlat(flat):
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	flat = decodeUrlText(flat)

	conn = sqlite3.connect('data/data.db')
	conn.execute("UPDATE homeOwns SET flat_no='"+flat+"' WHERE aptNo='"+uid+"'")
	conn.commit()
	conn.close()

	return "success"

@app.route('/editHomeOwnName/<name>')
def editHomeOwnName(name):
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	name = decodeUrlText(name)

	conn = sqlite3.connect('data/data.db')
	conn.execute("UPDATE homeOwns SET usrName='"+name+"' WHERE aptNo='"+uid+"'")
	conn.commit()
	conn.close()

	return "success"

@app.route('/editHomeOwnEmail/<email>')
def editHomeOwnEmail(email):
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	email = decodeUrlText(email)

	conn = sqlite3.connect('data/data.db')
	conn.execute("UPDATE homeOwns SET email='"+email+"' WHERE aptNo='"+uid+"'")
	conn.commit()
	conn.close()

	return "success"

@app.route('/editHomeOwnPhone/<phone>')
def editHomeOwnPhone(phone):
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	phone = decodeUrlText(phone)

	conn = sqlite3.connect('data/data.db')
	conn.execute("UPDATE homeOwns SET phone='"+phone+"' WHERE aptNo='"+uid+"'")
	conn.commit()
	conn.close()

	return "success"

@app.route('/editHomeOwnDob/<dob>')
def editHomeOwnDob(dob):
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	dob = decodeUrlText(dob)

	conn = sqlite3.connect('data/data.db')
	conn.execute("UPDATE homeOwns SET dob='"+dob+"' WHERE aptNo='"+uid+"'")
	conn.commit()
	conn.close()

	return "success"

@app.route('/editHomeOwnFather/<father>')
def editHomeOwnFather(father):
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	father = decodeUrlText(father)

	conn = sqlite3.connect('data/data.db')
	conn.execute("UPDATE homeOwns SET father='"+father+"' WHERE aptNo='"+uid+"'")
	conn.commit()
	conn.close()

	return "success"

@app.route('/editHomeOwnMother/<mother>')
def editHomeOwnMother(mother):
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	mother = decodeUrlText(mother)

	conn = sqlite3.connect('data/data.db')
	conn.execute("UPDATE homeOwns SET mother='"+mother+"' WHERE aptNo='"+uid+"'")
	conn.commit()
	conn.close()

	return "success"

@app.route('/editHomeOwnOccup/<occup>')
def editHomeOwnOccup(occup):
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	occup = decodeUrlText(occup)

	conn = sqlite3.connect('data/data.db')
	conn.execute("UPDATE homeOwns SET occupation='"+occup+"' WHERE aptNo='"+uid+"'")
	conn.commit()
	conn.close()

	return "success"

@app.route('/editHomeOwnCommAddr/<addr>')
def editHomeOwnCommAddr(addr):
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	addr = decodeUrlText(addr)

	conn = sqlite3.connect('data/data.db')
	conn.execute("UPDATE homeOwns SET comm_address='"+addr+"' WHERE aptNo='"+uid+"'")
	conn.commit()
	conn.close()

	return "success"

@app.route('/editHomeOwnPermAddr/<addr>')
def editHomeOwnPermAddr(addr):
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	addr = decodeUrlText(addr)

	conn = sqlite3.connect('data/data.db')
	conn.execute("UPDATE homeOwns SET perm_address='"+addr+"' WHERE aptNo='"+uid+"'")
	conn.commit()
	conn.close()

	return "success"

@app.route('/editHomeOwnOccupancy/<occu>')
def editHomeOwnOccupancy(occu):
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	occu = decodeUrlText(occu)

	conn = sqlite3.connect('data/data.db')
	conn.execute("UPDATE homeOwns SET occupancy="+occu+" WHERE aptNo='"+uid+"'")
	conn.commit()
	conn.close()

	return "success"

@app.route('/editHomeOwnPhoto', methods = ['GET', 'POST'])
def editHomeOwnPhoto():
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	if request.method == 'POST':
		photo = request.files['photoFile']

		i = 0
		while (True):
			fname = "static/images/homeOwns/"+secure_filename(uid)+"/photo"+str(i)+"." + photo.filename.split('.')[-1]
			if not os.path.exists(fname):
				break
			i += 1

		photo.save(fname)

		conn = sqlite3.connect('data/data.db')

		conn.execute("UPDATE homeOwns SET photo='/"+fname+"' WHERE aptNo='"+uid+"'")
		conn.commit()
		conn.close()

		return redirect(url_for("homeOwner"))

	return "oops"

@app.route('/uploadHomeOwnIdProof', methods = ['GET', 'POST'])
def uploadHomeOwnIdProof():
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	if request.method == 'POST':
		photo = request.files['photoFile']

		i = 0
		while (True):
			fname = "static/images/homeOwns/"+secure_filename(uid)+"/idProof"+str(i)+"." + photo.filename.split('.')[-1]
			if not os.path.exists(fname):
				break
			i += 1

		photo.save(fname)

		conn = sqlite3.connect('data/data.db')

		conn.execute("UPDATE homeOwns SET id_photo='/"+fname+"' WHERE aptNo='"+uid+"'")
		conn.commit()
		conn.close()

		return redirect(url_for("homeOwner"))

	return "oops"

@app.route('/uploadHomeOwnCommAddrProof', methods = ['GET', 'POST'])
def uploadHomeOwnCommAddrProof():
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	if request.method == 'POST':
		photo = request.files['photoFile']

		i = 0
		while (True):
			fname = "static/images/homeOwns/"+secure_filename(uid)+"/commAddrProof"+str(i)+"." + photo.filename.split('.')[-1]
			if not os.path.exists(fname):
				break
			i += 1

		photo.save(fname)

		conn = sqlite3.connect('data/data.db')

		conn.execute("UPDATE homeOwns SET comm_add_proof='/"+fname+"' WHERE aptNo='"+uid+"'")
		conn.commit()
		conn.close()

		return redirect(url_for("homeOwner"))

	return "oops"

@app.route('/uploadHomeOwnPermAddrProof', methods = ['GET', 'POST'])
def uploadHomeOwnPermAddrProof():
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	if request.method == 'POST':
		photo = request.files['photoFile']

		i = 0
		while (True):
			fname = "static/images/homeOwns/"+secure_filename(uid)+"/permAddrProof"+str(i)+"." + photo.filename.split('.')[-1]
			if not os.path.exists(fname):
				break
			i += 1

		photo.save(fname)

		conn = sqlite3.connect('data/data.db')

		conn.execute("UPDATE homeOwns SET perm_add_proof='/"+fname+"' WHERE aptNo='"+uid+"'")
		conn.commit()
		conn.close()

		return redirect(url_for("homeOwner"))

	return "oops"

@app.route('/uploadHomeOwnSaleDeed', methods = ['GET', 'POST'])
def uploadHomeOwnSaleDeed():
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	if request.method == 'POST':
		photo = request.files['photoFile']

		i = 0
		while (True):
			fname = "static/images/homeOwns/"+secure_filename(uid)+"/saleDeed"+str(i)+"." + photo.filename.split('.')[-1]
			if not os.path.exists(fname):
				break
			i += 1

		photo.save(fname)

		conn = sqlite3.connect('data/data.db')

		conn.execute("UPDATE homeOwns SET sale_deed='/"+fname+"' WHERE aptNo='"+uid+"'")
		conn.commit()
		conn.close()

		return redirect(url_for("homeOwner"))

	return "oops"

@app.route('/addTenant/<name>')
def addTenant(name):
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	name = decodeUrlText(name)

	conn = sqlite3.connect('data/data.db')

	conn.execute("INSERT INTO tenants(name) VALUES ('"+name+"')")

	cursor = conn.execute("SELECT MAX(tenant_id) FROM tenants")

	for row in cursor:
		tid = str(row[0])

	conn.execute("INSERT INTO apt_tenant VALUES ('"+uid+"', "+tid+")")

	conn.commit()
	conn.close()

	os.mkdir("static/images/tenants/"+tid)

	return "success:"+tid

@app.route('/removeTenant/<tid>')
def removeTenant(tid):
	if 'user' in session:
		uid = session['user']
	else:
		return redirect(url_for('login'))

	conn = sqlite3.connect('data/data.db')

	cursor = conn.execute("SELECT * FROM apt_tenant WHERE aptNo='"+uid+"' AND tenant_id="+tid)

	cursor = cursor.fetchall()

	if len(cursor) == 0:
		return redirect(url_for('login'))

	shutil.rmtree("static/images/tenants/"+tid)

	conn.execute("DELETE FROM apt_tenant WHERE tenant_id="+tid)
	conn.execute("DELETE FROM tenants WHERE tenant_id="+tid)
	conn.commit()
	conn.close()

	return "success"



@app.route('/viewIncomeExpenditure')
def viewIncomeExpenditure():

	today = datetime.today()
	year = today.year
	month = today.month
	monthNum = (year - 1970) * 12 + month

	conn = sqlite3.connect('data/data.db')

	cursor = conn.execute("SELECT type, SUM(amount) FROM income WHERE month="+str(monthNum)+" GROUP BY type")

	income = "<table width='300px' cellpadding='5'>\n<tr>\n<th><center>Type</center></th>\n<th><center>Amount</center></th>\n</tr>\n"
	incTot = 0

	for row in cursor:
		income += "<tr>\n<td><center>"+str(row[0])+"</center></td>\n<td><center>&#8377; "+str(row[1])+"</center></td>\n</tr>\n"
		incTot += row[1]

	income += "<tr>\n<th><center>Total</center></th>\n<th><center>&#8377; "+str(incTot)+"</center></th>\n</tr>\n</table>"


	cursor = conn.execute("SELECT category, SUM(amount) FROM expense WHERE month="+str(monthNum)+" GROUP BY category")

	expense = "<table width='300px' cellpadding='5'>\n<tr>\n<th><center>Category</center></th>\n<th><center>Amount</center></th>\n</tr>\n"
	expTot = 0

	for row in cursor:
		expense += "<tr>\n<td><center>"+str(row[0])+"</center></td>\n<td><center>&#8377; "+str(row[1])+"</center></td>\n</tr>\n"
		expTot += row[1]

	expense += "<tr>\n<th><center>Total</center></th>\n<th><center>&#8377; "+str(expTot)+"</center></th>\n</tr>\n</table>"

	monthNet = "<strong>Net income this month: &#8377; "+str(incTot - expTot)+"</strong>"

	return render_template('incExp.html', income = income, expense = expense, monthNet = monthNet)


@app.route('/financialStatus')
def financialStatus():

	conn = sqlite3.connect('data/data.db')

	cursor = conn.execute("SELECT type, SUM(amount) FROM income GROUP BY type")

	income = "<table width='300px' cellpadding='5'>\n<tr>\n<th><center>Type</center></th>\n<th><center>Amount</center></th>\n</tr>\n"
	incTot = 0

	for row in cursor:
		income += "<tr>\n<td><center>"+str(row[0])+"</center></td>\n<td><center>&#8377; "+str(row[1])+"</center></td>\n</tr>\n"
		incTot += row[1]

	income += "<tr>\n<th><center>Total</center></th>\n<th><center>&#8377; "+str(incTot)+"</center></th>\n</tr>\n</table>"


	cursor = conn.execute("SELECT category, SUM(amount) FROM expense GROUP BY category")

	expense = "<table width='300px' cellpadding='5'>\n<tr>\n<th><center>Category</center></th>\n<th><center>Amount</center></th>\n</tr>\n"
	expTot = 0

	for row in cursor:
		expense += "<tr>\n<td><center>"+str(row[0])+"</center></td>\n<td><center>&#8377; "+str(row[1])+"</center></td>\n</tr>\n"
		expTot += row[1]

	expense += "<tr>\n<th><center>Total</center></th>\n<th><center>&#8377; "+str(expTot)+"</center></th>\n</tr>\n</table>"

	finStat = "<strong>Net balance amount: &#8377; "+str(incTot - expTot)+"</strong>"

	return render_template('financialStatus.html', income = income, expense = expense, finStat = finStat)


@app.route('/viewMaintenance')
def viewMaintenance():

	conn = sqlite3.connect('data/data.db')

	cursor = conn.execute("SELECT COUNT(user_id) FROM users")

	cursor = cursor.fetchall()

	totApts = cursor[0][0]

	today = datetime.today()
	year = today.year
	month = today.month
	monthNum = (year - 1970) * 12 + month

	maintDets = "<table width='500px' cellpadding='5'>\n<tr>\n<th><center>Apartment</center></th>\n<th><center>Status</center></th>\n</tr>\n"

	cursor = conn.execute("SELECT user_id FROM users")

	totPaid = 0

	for row in cursor:

		aptNo = row[0]

		maintDets += "<tr>\n<td><center>"+aptNo+"</center></td>\n"

		cursor2 = conn.execute("SELECT * FROM apartments WHERE aptNo='"+aptNo+"'")

		cursor2 = cursor2.fetchall()

		regMonth = cursor2[0][1]

		maintAmt = cursor2[0][5] * 5 + cursor2[0][6] * 100

		cursor2 = conn.execute("SELECT * FROM Maint_"+aptNo.replace("-", "_").replace("/", "_"))

		cursor2 = cursor2.fetchall()

		if len(cursor2) != 0:
			lastMonth = cursor2[-1][0]
		else:
			lastMonth = regMonth - 1

		toPay = monthNum - lastMonth

		paid = toPay * maintAmt * -1

		totPaid += paid

		if toPay > 0:
			maintDets += "<td style='color: red'><center>Dues: " + str(toPay) + " months (&#8377; "+str(paid)+"/-)</center></td>\n"
		elif toPay == 0:
			maintDets += "<td style='color: blue'><center>Settled up</center></td>\n"
		else:
			maintDets += "<td style='color: green'><center>Advance payment: " + str(-1 * toPay) + " months (&#8377; "+str(paid)+"/-)</center></td>\n"

		maintDets += "</tr>\n"

	maintDets += "</table>\n<br><br>\n"

	if totPaid < 0:
		maintDets += "<strong style='color: red'>Total: &#8377; "+str(totPaid)+"/-</strong>"
	elif totPaid == 0:
		maintDets += "<strong style='color: blue'>Total: &#8377; "+str(totPaid)+"/-</strong>"
	else:
		maintDets += "<strong style='color: green'>Total: &#8377; "+str(totPaid)+"/-</strong>"

	return render_template('viewMaintenance.html', totApts = totApts, maintDets = maintDets)

# @app.route('/payment')
# def payment():
# 	if 'user' in session:
# 		uid = session['user']
# 	else:
# 		return redirect(url_for('login'))

# 	today = datetime.today()
# 	year = today.year
# 	month = today.month
# 	monthNum = (year - 1970) * 12 + month

# 	conn = sqlite3.connect('data/data.db')

# 	cursor = conn.execute("SELECT * FROM apartments WHERE aptNo='"+uid+"'")

# 	cursor = cursor.fetchall()

# 	regMonth = cursor[0][1]

# 	maintAmt = cursor[0][5] * 5 + cursor[0][6] * 100

# 	cursor = conn.execute("SELECT * FROM Maint_"+uid.replace("-", "_").replace("/", "_"))

# 	cursor = cursor.fetchall()

# 	if len(cursor) != 0:
# 		lastMonth = cursor[-1][0]
# 	else:
# 		lastMonth = regMonth - 1

# 	toPay = monthNum - lastMonth

# 	if toPay > 0:
# 		payDet = "You need to <strong>pay</strong> maintenance for <strong>" + str(toPay) + " months</strong>."
# 	elif toPay == 0:
# 		payDet = "Your maintenance payment is <strong>settled up!</strong>"
# 	else:
# 		payDet = "You have paid maintenance for <strong>" + str(-1 * toPay) + " months</strong> in <strong>advance</strong>."

# 	return render_template('payment.html', user = uid, payDet = payDet, maintAmt = maintAmt)


if (__name__ == "__main__"):
	app.run(port = 5000)
