from flask import Flask, render_template, redirect, request, flash, session
from flask_app import app
from flask_app.controllers.users import dashboard
from flask_app.models import account
from flask_app.models import user
from flask_app.models import company 
from flask_app.models import api


# RENDER ROUTES -------------------------------

@app.route('/companies/<int:id>')
def show_one(id):
    if not user.User.is_logged_in():
        flash("Must be logged in to access this page")
        return redirect("/")
    
    data = {"id" : id}
    cached_company = company.Company.get_company(data)
    current_user = user.User.get_user_all({"id" : session['user_id']})
    
    return render_template('show_company.html', cached_company = cached_company, current_user = current_user)





#  ACTION ROUTES ------------------------------

@app.route('/add_company_by_ticker', methods = ["POST"])
def add_company():
    if not user.User.is_logged_in():
        flash("Must be logged in to access this page")
        return redirect("/")
    input = request.form.getlist("symbol")
    new_company = api.check_company_data(input[0])
    company.Company.create_one(new_company)

    return redirect('/dashboard')

@app.route('/companies/remove/<int:id>')
def remove_company(id):
    company.Company.delete({"id" : id})
    return redirect("/dashboard")

@app.route('/companies/<int:id>/update_price', methods = ['POST'])
def update_price(id):
    print(request.form)
    company.Company.Update_company_prices(request.form)
    return redirect(f'/companies/{id}')
    
