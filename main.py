from flask import Flask, render_template, request,session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
from datetime import datetime

with open('config.json', 'r') as c:
    parameters= json.load(c)['parameters']
local_server = True

app = Flask(__name__)
app.secret_key='super-secrete-key'
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=parameters['gmail-user'],
    MAIL_PASSWORD=parameters['gmail-password']
)
mail = Mail(app)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:@localhost/hotel'
db = SQLAlchemy(app)


class BookTable(db.Model):
    '''sno, name, email,phone_num, date,time,nopeople, msg'''

    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=False, nullable=False)
    phone_num = db.Column(db.String(80), unique=False, primary_key=True)
    date = db.Column(db.String(80), unique=False, nullable=False)
    time = db.Column(db.String(80), unique=False, nullable=False)
    nopeople = db.Column(db.Integer, unique=False, nullable=False)
    msg = db.Column(db.String(80), unique=False, nullable=False)

class Connect(db.Model):
    '''sno, name, email,subject, msg'''

    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=False, nullable=False)
    subject = db.Column(db.String(80), unique=False, primary_key=True)
    message = db.Column(db.String(80), unique=False, nullable=False)



@app.route("/")
def home():

    return render_template('home.html')

@app.route("/admin",methods=['GET','POST'])
def login():
    if request.method=='POST':
        if 'user' in session or session==parameters['admin_user']:
            data=BookTable.query.all()
            value=Connect.query.all()
            return render_template('dashboard.html', parameters=parameters,tbookings=data,creq=value)

        username=request.form.get('username')
        userpass=request.form.get('password')
        if username==parameters['admin_user'] and userpass == parameters['admin_password']:
            session['user']=username
            data = BookTable.query.all()
            value = Connect.query.all()
            return render_template('dashboard.html',parameters=parameters,tbookings=data,creq=value)


    return render_template('login.html')

@app.route("/table", methods=['GET','POST'])
def tablebook():
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        date = request.form.get('date')
        time = request.form.get('time')
        people = request.form.get('people')
        message = request.form.get('message')
        # leftside=databasevariable
        entry = BookTable(name=name, phone_num=phone,email=email, date=date,time=time, nopeople=people, msg=message )
        db.session.add(entry)
        db.session.commit()
        # mail.send_message('New Table Booking Request from  ' + name,
        #                   sender=email,
        #                   recipients=[parameters['gmail-user']],
        #                   body=message+"\n"+'Date='+date +"\n"+ 'Time='+time+  "\n" + phone+"\n"+email)

    return "Your booking request was sent. We will call back or send an Email to confirm your reservation. Thank you!"


@app.route("/connect",methods=['GET','POST'])
def connect():
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        # leftside=databasevariable
        dataentry = Connect(name=name, email=email, subject=subject, message=message)
        db.session.add(dataentry)
        db.session.commit()
        # print ("We will get back to you Shortly Thank you for Contacting us")
        # mail.send_message('New Contact Request from  ' + name,
        #                   sender=email,
        #                   recipients=[parameters['gmail-user']],
        #                   body="Subeject:"+subject+"\n"+
        #                        message+"\n"
        #                        +'Date='+date+"\n"
        #                        + 'Time='+time+  "\n" + phone+"\n"+email)


    return " Your Contact request has been sent. Our team will contact you very soon .Thank You"

@app.route("/logout")
def logout():
    session.pop('user')

    return render_template('home.html')

app.run(debug=True)
