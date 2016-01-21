import urllib2,json
import hashlib
from flask import Flask, render_template, session, request, redirect, url_for
from database import *
import utils

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
@app.route("/home",methods=["GET","POST"])
def home():
    if request.method == "GET":
        loggedin = False
        if 'username' in session:
            loggedin = True
            username = session['username']
        movies = utils.getNowPlaying()
        movieimages = []
        movienames = []
        for i in movies:
            movienames.append(i['name'])
            movieimages.append(i['poster'])
        return render_template("home.html",loggedin=loggedin,movieimages=movieimages,movienames=movienames)
    else:
        button = request.form['button']
        if button == "login":
            return redirect(url_for("login"))
        elif button == "create_account":
            return redirect(url_for("create_account"))
        elif button == "edit_account":
            return redirect(url_for("edit_account"))
        else:
            return redirect(url_for("find_tickets"))
    
@app.route("/login", methods=["GET","POST"])
@app.route("/login/", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form['username']
        password = request.form['password']

        m = hashlib.md5()
        m.update(password)
        passhash = m.hexdigest()

        if authenticate(username, passhash):

            session["username"] = username
            return redirect(url_for("home", username = username))
        else:
            error = "Invalid username and password combination"
            return render_template("login.html", err = error, s = session)


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
    app.secret_key = "lolsup"
    app.run(host='0.0.0.0',port=8000)


##google maps key:AIzaSyCks4P7pW9w_neGLaRCHZnrcuwUwIppEtc
