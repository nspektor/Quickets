import urllib2,json
import hashlib
from flask import Flask, render_template, session, request, redirect, url_for
from database import *

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
@app.route("/home",methods=["GET","POST"])
def home():
   # if request.method == "GET":
    return render_template("home.html")
#    else:
 #       payload = {'X-AMC-Vendor-Key':'451EB6B4-E2FD-412E-AF07-CA640853CDC3'}
 #       r = requests.post("https://api.amctheatres.com/v2/movies",data=payload)
  #      print r

@app.route("/login", methods=["GET","POST"])
@app.route("/login/", methods=["GET","POST"])
def login():
    return render_template("login.html")

@app.route("/create_account", methods=["GET","POST"])
@app.route("/create_account/", methods=["GET","POST"])
def create_account():
    if request.method == "GET":
        return render_template("create_account.html")
    else:
        username = request.form['username']
        password = request.form['password']

        if " " in username or "\t" in username:
            error = "You cannot have spaces in your username!"
            return render_template("create_account.html", err = error, s = session)
        if (password == ""):
            error = "You cannot have no password!"
            return render_template("create_account.html", err = error, s = session)
        if " " in password or "\t" in password:
            error = "You cannot have spaces in your password!"
            return render_template("create_account.html", err = error, s = session)
        m = hashlib.md5()
        m.update(password)
        passhash = m.hexdigest()
        if (newUser(username, passhash)):
            smsg = "You will be redirected to the log-in page in a moment."
            return render_template("login.html", success = smsg, s = session);

        error = "Username already in use!"
        return render_template("create_account.html", err = error, s = session)

@app.route("/edit_account", methods=["GET","POST"])
@app.route("/edit_account/", methods=["GET","POST"])
def edit_account():
    return render_template("edit_account.html")

@app.route("/find_tickets", methods=["GET","POST"])
@app.route("/find_tickets/", methods=["GET","POST"])
def find_tickets():
    return render_template("find_tickets.html")


if __name__=="__main__":
    app.debug = True
    app.run(host='0.0.0.0',port=8000)


##google maps key:AIzaSyCks4P7pW9w_neGLaRCHZnrcuwUwIppEtc
