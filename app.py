import urllib2,json
from flask import Flask, render_template, session, request, redirect, url_for

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
    return render_template("create_account.html")

@app.route("/find_tickets", methods=["GET","POST"])
@app.route("/find_tickets/", methods=["GET","POST"])
def find_tickets():
    return render_template("find_tickets.html")
                                         
    
if __name__=="__main__":
    app.debug = True
    app.run(host='0.0.0.0',port=8000)


##google maps key:AIzaSyCks4P7pW9w_neGLaRCHZnrcuwUwIppEtc
