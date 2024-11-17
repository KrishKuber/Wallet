import os
from datetime import datetime
import re
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify, make_response
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date

def change_date_format(dt):
        return re.sub(r'(\d{4})-(\d{1,2})-(\d{1,2})', '\\3/\\2/\\1', dt)
        
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///wallet.db")

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


registerer = False
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        global registerer
        if(registerer == True):
            registerer = False
            #Getting form info
            username = request.form.get("username")
            password = request.form.get("password")

            #Hashing password
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

            #Storing into table
            db.execute("Insert into users(username,hash) values(?,?)",username,hashed_password)

            # Query database for username
            rows = db.execute("SELECT * FROM users WHERE username = ?", username)

            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]
            # Redirect user to home page
            return redirect("/dashboard")
        registerer = False
        return redirect("/register")


@app.route("/register/check", methods=["POST"])
def check():
    #req is the string username
    req = request.form['username']
    #Checking if username exists
    check = db.execute("Select * from users where username=?", req)
    if check:
        if req == check[0]['username']:
            return jsonify({"error" : 1})
    global registerer
    registerer = True
    return jsonify({"error" : 2})

@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/login", methods=["POST", "GET"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", error="Invalid username and/or password")
        else:
            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]
            # Redirect user to home page
            return redirect("/dashboard")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/table", methods=["POST", "GET"])
def table():
    if request.method == "GET":
        user_id = session["user_id"]
        records = db.execute("Select * from records where id=? order by date DESC",user_id)
        return render_template("table.html", records=records)
    else:
        item = request.form.get("item").upper()
        price = request.form.get("price").upper()
        category = request.form.get("category").upper()
        mode = request.form.get("mode").upper()
        odate = request.form.get("date")
        user_id = session["user_id"]
        date = change_date_format(odate)
        #Storing into table
        db.execute("Insert into records(id,date,item,price,category,mode) values(?,?,?,?,?,?)",user_id,date,item,price,category,mode)
        records = db.execute("Select * from records where id=? order by date DESC",session["user_id"])
        return render_template("table.html", records=records)

@app.route("/table/delete", methods=["POST"])
def delete_table():
    recordid = request.form.get("recordid")
    db.execute("DELETE FROM records WHERE record_id=?", recordid)
    records = db.execute("Select * from records where id=?",session['user_id'])
    return render_template("table.html", records=records)

@app.route("/table/date", methods=["POST"])
def searchd():
    odate = request.form.get("sdate")
    date = change_date_format(odate)
    records = db.execute("Select * from records where (id=? and date=?)",session['user_id'],date)
    return render_template("table.html", records=records)
@app.route("/table/item", methods=["POST"])

@app.route("/table/item", methods=["POST"])
def searchi():
    item = request.form.get("sitem").upper()
    records = db.execute("Select * from records where (id=? and item like ?)",session['user_id'],'%' + item  + '%')
    return render_template("table.html", records=records)
    
@app.route("/table/price", methods=["POST"])
def searchp():
    item = request.form.get("sprice")
    records = db.execute("Select * from records where (id=? and price=?)",session['user_id'],item)
    return render_template("table.html", records=records)
    
@app.route("/table/category", methods=["POST"])
def searchc():
    item = request.form.get("scategory").upper()
    records = db.execute("Select * from records where (id=? and category like ?)",session['user_id'],'%' + item  + '%')
    return render_template("table.html", records=records)
    
@app.route("/table/mode", methods=["POST"])
def searchm():
    item = request.form.get("smode").upper()
    records = db.execute("Select * from records where (id=? and mode like ?)",session['user_id'],'%' + item  + '%')
    return render_template("table.html", records=records)
    
@app.route("/texpense", methods=["POST", "GET"])
def texpense():
    if request.method == "GET":
        today = date.today()

        d2 = today.strftime("%d/%m/%Y")
        records = db.execute("Select * from records where id=? and date=?",session['user_id'],d2)
        
        total = 0.0
        for record in records:
            total = total + record['price']
        return render_template("texpense.html", records=records, total=total)
    else:
        item = request.form.get("item").upper()
        price = request.form.get("price").upper()
        category = request.form.get("category").upper()
        mode = request.form.get("mode").upper()

        today = date.today()

        d1 = today.strftime("%d/%m/%Y")
        user_id = session["user_id"]
        #Storing into table
        db.execute("Insert into records(id,date,item,price,category,mode) values(?,?,?,?,?,?)",user_id,d1,item,price,category,mode)
        records = db.execute("Select * from records where id=? and date=?",user_id,d1)
        total = 0.0
        for record in records:
            total = total + record['price']
        return render_template("texpense.html", records=records, total=total)

@app.route("/texpense/delete", methods=["POST"])
def delete():
    recordid = request.form.get("recordid")
    db.execute("DELETE FROM records WHERE record_id=?", recordid)
    today = date.today()

    d3 = today.strftime("%d/%m/%Y")
    records = db.execute("Select * from records where id=? and date=?",session['user_id'],d3)
    total = 0.0
    for record in records:
        total = total + record['price']
    return render_template("texpense.html", records=records, total=total)

@app.route("/dashboard")
def dashboard():
    if session:
        userid = session["user_id"]
        user = db.execute("Select username from users where id=?", userid)
        username = user[0]['username']
        today = date.today()
        montho = today.strftime('%m')
        yearo = today.strftime('%Y')
        records = db.execute("Select * from records where substr(date, 4, 2) = ? and id = ?" , montho,session['user_id'])
        print(session['user_id'])
        print(records)
        total = 0.0
        for record in records:
            total += record['price']
        print(total)
        month = int(montho)
        year = int(yearo)
        year1 = year
        if month == 1:
            month1 = 10
            year1 = year - 1
        elif month == 2:
            month1 = 11
            year1 = year - 1
        elif month == 3:
            month1 = 12
            year1 = year - 1
        else:
            month1 = month - 3
        year1n = str(year1)    
        month1n = str(month1)
        
        year2 = year
        month2 = 0
        if month == 1:
            month2 = 11
            year2 = year - 1
        elif month == 2:
            month2 = 12
            year2 = year - 1
        else:
            month2 = month - 2
        year2n = str(year2)    
        month2n = str(month2)
        
        month3 = 0
        year3 = year
        if month == 1:
            month2 = 12
            year3 = year - 1
        else:
            month3 = month - 1
        year3n = str(year3)    
        month3n = str(month3)
        
        records1 = db.execute("Select price from records where substr(date, 4, 2) = ? and substr(date, 7, 4) = ? and id = ?" , month1n,year1n,session['user_id'])
        print(records1)
        records2 = db.execute("Select price from records where substr(date, 4, 2) = ? and substr(date, 7, 4) = ? and id = ?" , month2n,year2n,session['user_id'])
        records3 = db.execute("Select price from records where substr(date, 4, 2) = ? and substr(date, 7, 4) = ?and id = ?" ,month3n,year3n,session['user_id'])
        print(records2)
        print(records3)
        total1 = 0.0
        if records1 != None:    
            for record in records1:
                total1 = total1 + record['price']
            
        total2 = 0.0
        if records2 != None:
            for record in records2:
                total2 = total2 + record['price']
            
        total3 = 0.0
        if records3 != None:
            for record in records3:
                total3 = total3 + record['price']
                
        print(total1, total2, total3)        
        
        average = (total1 + total2 + total3) / 3.0
        
        
        entries = db.execute("Select * from records where id = ? order by date DESC limit 10", session['user_id'])
        
    
        return render_template("dashboard.html", username=username,total=total,average=round(average, 2), entries = entries)
    return redirect("/")





