from flask_app import app
from flask_app.controllers import users, positions, orders, companies, accounts






if __name__ == "__main__":
    app.run(debug=True)