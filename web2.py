# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 14:52:17 2023

@author: Dr. Bhargavi B
"""

# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template,request,session
import ibm_db
#

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
app.secret_key = "_ab+d=5"
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=fbd88901-ebdb-4a4f-a32e-9822b9fb237b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32731;UID=brf89243;PWD=eS3cKktgFZdTYWsM;SECURITY=SSL;SSLCERTIFICATE=DigiCertGlobalRootCA.crt", '','')
print(ibm_db.active(conn))
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        global uname
        uname = request.form['username']
        pword = request.form['password']
        print(uname, pword)
        sql = "SELECT * FROM REGISTER_GITAM WHERE USERNAME = ? AND PASSWORD = ?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt, 1, uname)
        ibm_db.bind_param(stmt,2,pword)
        ibm_db.execute(stmt)
        out = ibm_db.fetch_assoc(stmt)
        print(out)
        if out != False:
            session['username'] = uname
            session['emailid'] = out['EMAILID']
            
            if out['ROLE'] == 0:
                return render_template("templates/adminprofile.html",username = uname, emailid = out['EMAILID'] )
            elif out['ROLE'] == 1:
                return render_template("templates/studentprofile.html",username = uname, emailid = out['EMAILID'])
            else: 
                return render_template("templates/facultyprofile.html",username = uname, emailid = out['EMAILID'])
        else: 
            msg = "Invalid Credentials"
            return render_template("login.html",message1= msg)
    return render_template("login.html")

# main driver function
if __name__ == '__main__':

	# run() method of Flask class runs the application
	# on the local development server.
	app.run(debug=True)
