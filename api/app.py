from flask import Flask,request,redirect,url_for,render_template,make_response
from datetime import datetime
app=Flask(__name__,template_folder="templates")
users={}
statements={}
@app.route("/")
def home():
    return render_template ("welcome.html")

@app.route("/reg",methods=["GET","POST"])
def reg():
    if request.method=="POST":
        print(request.form)
        username=request.form.get("username")
        useremail=request.form.get("useremail")
        userpassword=request.form.get("userpassword")
        userpin=request.form.get("userpin")
        if username not in users:
            users[username]={"email":useremail,"password":userpassword,"pin":userpin,"Amount":0}
            if username not in statements:
                statements[username]={"deposit_statements":[],"withdraw_statements":[]}
                print(statements[username])
            else:
                return redirect(url_for("login"))
        else: 
            return "user name already existed"
    return render_template("reg.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":  
        login_username=request.form["username"]
        login_password=request.form["userpassword"]
        if login_username in users:
            if login_password==users[login_username]['password']:
                resp=make_response(redirect(url_for("dashboard"))) # create response object to set cokiee
                resp.set_cookie("user",login_username) # creating cookie key-value pair using resp object
                return resp
            else:
                return "invalid password"
        else:
            return "invalid username"
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if request.cookies.get("user"):
        return render_template("dashboard.html")
    else:
        return redirect(url_for('login'))

@app.route("/deposit",methods=["GET","POST"])
def deposit():
    if request.cookies.get("user"):
        if request.method=="POST":
            deposit_amt=int(request.form["deposit_amt"])
            username=request.cookies.get("user")
            if deposit_amt>0:
                if deposit_amt%100==0:
                    if deposit_amt<=50000:
                        users[username]["Amount"] +=deposit_amt
                        deposit_time=datetime.now()
                        deposit_data=(deposit_amt,deposit_time)
                        statements[username]["deposit_statements"].append(deposit_data)
                        # return redirect(url_for('balance'))
                    else:
                        return f"amount exceed than 50000"
                else:
                    return f" amount must be multiple of 100"
            else:
                return f"deposit amount must be greater than 0"
        return render_template("deposit.html")
    else:
        return redirect(url_for("login"))    

@app.route("/withdraw",methods=["GET","POST"])
def withdraw():
    if request.cookies.get("user"):
        if request.method=="POST":
            withdraw_amt=int(request.form["withdraw_amt"])
            username=request.cookies.get("user")
            balance_amount=users[username]["Amount"]
            if withdraw_amt>0:
                if withdraw_amt%100==0:
                    if withdraw_amt<=balance_amount:
                        users[username]["Amount"]-=withdraw_amt
                        withdraw_time=datetime.now()
                        withdraw_data=(withdraw_amt,withdraw_time)
                        statements[username]["withdraw_statements"].append(withdraw_data)
                        # return redirect(url_for('balance'))        
                    else: 
                        return "Entered amount not sufficient"
                else:
                    return f"withdraw amount must be multiple of 100"
            else:
                return f"withdraw amount must be greater than 0"
        return render_template("withdraw.html")
    else:
        return redirect(url_for("login")) 

@app.route("/balance")
def balance():
    if request.cookies.get("user"):
        username=request.cookies.get("user")
        balance_amt=users[username]['Amount']
        return render_template("balance.html",balance_amt=balance_amt)
    else:
        return redirect(url_for("login"))

# @app.route("/dummy")
# def dummy():
#     print(users)
#     return render_template("dummy.html",users=users)

@app.route("/userstatements")
def userstatements():
    if request.cookies.get("user"):
        username=request.cookies.get("user")
        deposit_userstatements=statements[username]["deposit_statements"]
        withdraw_userstatements=statements[username]["withdraw_statements"]
        return render_template("statements.html",deposit_userstatements=deposit_userstatements,withdraw_userstatements=withdraw_userstatements)
    else:
        return redirect(url_for("login"))

@app.route("/userlogout")
def userlogout():
    if request.cookies.get("user"):
        username=request.cookies.get("user")
        resp=make_response(redirect(url_for("login")))
        resp.delete_cookie("user")
        return resp
    else:
        return redirect(url_for("login"))

if __name__=="__main__":
    app.run() 
app=app
    
    