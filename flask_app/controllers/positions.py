from flask import Flask, render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models import user
from flask_app.models import position
from flask_app.models import order


# RENDER ROUTES -------------------------------
@app.route('/positions/show')
def show_all_positions_by_account():
    positions = position.Position.show_all_by_account({"account_id" : 7})
    print(positions)
    return render_template('show_positions.html', positions = positions)




#  ACTION ROUTES ------------------------------