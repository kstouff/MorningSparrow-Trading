from flask import Flask, render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models import user 
from flask_app.models import company 
from flask_app.models import account 
from flask_app.models import order 
from flask_app.models import position 


# RENDER ROUTES -------------------------------



@app.route('/orders/confirmation/<int:account_id>/<int:company_id>')
def order_confirmation(account_id, company_id):
    

    current_user = user.User.get_user_all({"id" : session['user_id']})

    total_position = user.User.calculate_account_with_total_position(current_user, account_id, company_id)
    print(total_position)

    return render_template('order_confirmation.html', current_user = current_user, total_position = total_position, account_id = account_id)




#  ACTION ROUTES ------------------------------
@app.route('/orders/process', methods = ['POST'])
def process_order():
    print(request.form)
    current_order = order.Order.create_order(request.form)
    total_price = order.Order.calculate_purachase(request.form['share_num'], request.form['price_per_share'])
    print(total_price)
    data = {
        "id": request.form['account_id'], 
        "withdraw" : total_price
        }
    account.Account.withdraw(data)
    company.Company.caculate_updated_outstanding_shares(request.form['company_id'], request.form['share_num'])
    print(current_order)
    return redirect(f'/orders/confirmation/{request.form["account_id"]}/{request.form["company_id"]}')




