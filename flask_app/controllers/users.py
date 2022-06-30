from flask import Flask, render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models import user
from flask_app.models import company
from flask_app.models import account



# RENDER ROUTES -------------------

@app.route('/')
def index():
    
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    if not user.User.is_logged_in():
        flash("Must be logged in to access this page")
        return redirect("/")
    current_user = user.User.get_user_all({"id" : session["user_id"]})
    companies = company.Company.get_all_companies()
    # accounts = account.Account.get_accounts_by_user({"id" : session['user_id']})

    return render_template("dashboard.html", current_user = current_user, companies = companies)



@app.route('/user/account')
def edit_account():
    if not user.User.is_logged_in():
        flash("Must be logged in to access this page")
        return redirect("/")
    data = {"id" : session["user_id"]}
    users = user.User.get_user(data)

    return render_template('edit_account.html', users = users)
    




# ACTION ROUTES -------------------

@app.route('/user/create', methods = ["POST"])
def create_user():
    if user.User.registry_validator(request.form):
        user.User.create(request.form)
        flash("user successful created")
        return redirect ('/')
        
    return redirect("/")


@app.route('/user/login', methods = ["POST"])
def login():
    if not user.User.login_validator(request.form):
        return redirect('/')

    current_user = user.User.get_by_email(request.form)

    session["user_id"] = current_user.id

    return redirect("/dashboard")

@app.route('/user/update', methods = ["POST"])
def update_user():
    if not user.User.is_logged_in():
        flash("Must be logged in to access this page")
        return redirect("/")
    if user.User.update_validator(request.form):
        user.User.update(request.form)
        return redirect('/dashboard')
    return redirect('/user/account')

    
    pass


@app.route('/logout')
def log_out():
    session.clear()
    return redirect('/')

