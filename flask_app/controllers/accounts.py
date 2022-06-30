import re
from flask import Flask, render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models import user 
from flask_app.models import account 


# RENDER ROUTES -------------------------------

@app.route('/accounts/view/<int:id>')
def account_view(id):
    accounts = account.Account.get_with_order_totals({"id" : id})


    return render_template('show_positions.html', accounts = accounts)
    
    




#  ACTION ROUTES ------------------------------

@app.route('/accounts/create', methods = ['POST'])
def create_account():
    if not user.User.is_logged_in():
        flash("Must be logged in to access this page")
        return redirect("/")
    print(request.form)
    account.Account.create(request.form)
    return redirect('/dashboard')
    
@app.route('/accounts/delete', methods = ['POST'])
def delete_account():
    if not user.User.is_logged_in():
        flash("Must be logged in to access this page")
        return redirect("/")
    print(request.form)
    account.Account.delete(request.form)
    return redirect('/dashboard')


@app.route('/accounts/deposit', methods = ["POST"])
def deposit():
    if not user.User.is_logged_in():
        flash("Must be logged in to access this page")
        return redirect("/")
    data = {
        "id" : request.form['id'], 
        "deposit" : request.form['deposit'] 
    }
    temp_account = account.Account.deposit(data) 
    print(temp_account)
    return redirect('/dashboard')

@app.route('/accounts/withdraw', methods = ["POST"])
def withdraw():
    if not user.User.is_logged_in():
        flash("Must be logged in to access this page")
        return redirect("/")
    data = {
        "id" : request.form['id'], 
        "withdraw" : request.form['withdraw'] 
    }
    temp_account = account.Account.withdraw(data) 
    print(temp_account)
    return redirect('/dashboard')