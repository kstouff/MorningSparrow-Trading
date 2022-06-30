from audioop import avg
from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import position
from flask_app.models import account
from flask_app.models import order
from flask_app.models import company
from flask_app import app
from flask_bcrypt import Bcrypt
import re
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def create(cls, data):
        hash_browns = bcrypt.generate_password_hash(data['password'])
        hashed_dict = {
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "email": data["email"],
            "password": hash_browns
        }
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        print(query, hashed_dict)
        return connectToMySQL("trading_test").query_db(query, hashed_dict)

    @classmethod
    def get_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL("trading_test").query_db(query, data)

        if results:
            return cls(results[0])

    @classmethod
    def get_user_with_accounts(cls, data):
        query = "SELECT * FROM users left JOIN accounts on users.id = user_id WHERE users.id = %(id)s"
        mysql = connectToMySQL("trading_test")
        results = mysql.query_db(query, data)
        if results:    
            accounts = []
            for row in results:
                account_data = {
                    "id" : row["accounts.id"], 
                    "name" : row["name"],
                    "value" : row["value"],
                    "created_at" : row["accounts.created_at"],
                    "updated_at" : row["accounts.updated_at"],
                    "user_id" : row["user_id"]
                }
            accounts.append(account.Account(account_data))    
        
        return accounts        

    @classmethod
    def update(cls, data):

        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s;"
        connectToMySQL("trading_test").query_db(query, data)

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        connectToMySQL("trading_test").query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("trading_test").query_db(query, data)

        if results:
            return cls(results[0])




    
    @classmethod
    def get_user_all(cls, data):
        mysql = connectToMySQL("trading_test")
        query = 'Select * From users left join accounts on users.id = user_id left join orders on accounts.id = account_id left join companies on companies.id = company_id Where users.id = %(id)s;'
        results = mysql.query_db(query, data)
        all_users = []
        if results:
            for row in results:
                temp_user = cls(row)
                account_data = {
                    "id" : row["accounts.id"], 
                    "name" : row["name"],
                    "value" : row["value"],
                    "created_at" : row["accounts.created_at"],
                    "updated_at" : row["accounts.updated_at"],
                    "user_id" : row["user_id"]
                }
                order_data = {
                    "id" : row["orders.id"], 
                    "share_num" : row["share_num"],
                    "price_per_share" : row["price_per_share"],
                    "company_id" : row["company_id"],  
                    "created_at" : row["orders.created_at"],
                    "updated_at" : row["orders.updated_at"],
                    "account_id" : row["account_id"]
                }
                company_data = {
                    "id" : row["companies.id"],
                    "name" : row["companies.name"],
                    "share_num" : row["companies.share_num"],
                    "price_per_share" : row["price_per_share"],
                    "num_shares_outstanding" : row["num_shares_outstanding"],
                    "created_at" : row["companies.created_at"],
                    "updated_at" : row["companies.updated_at"],
                    "account_id" : row["account_id"]
                }
                temp_user.account = account.Account(account_data)
                temp_user.order = order.Order(order_data)
                temp_user.company = company.Company(company_data)

                all_users.append(temp_user)
        return all_users


    @classmethod
    def calculate_account_with_total_position(cls, profile, account_id, company_id):
        total_position_shares = 0
        total_position_value = 0

        
        for object in profile:
            if object.account.id == account_id and object.company.id == company_id:
                (total_position_shares) = int(total_position_shares) + int(object.order.share_num)
                (total_order_price) = int(object.order.share_num) * int(object.order.price_per_share)
                (total_position_value) = int(total_position_value) + int(total_order_price)

        avg_price_per_share = total_position_value/total_position_shares
        results = {
            "total_position_value" : total_position_value,
            "total_position_shares" : total_position_shares,
            "avg_price_per_share" : avg_price_per_share
        }
        return results


    

    @staticmethod
    def is_logged_in():
        if "user_id" in session:
            return True
        return False

    @staticmethod
    def login_validator(data):
        user = User.get_by_email(data)
        if not user:
            flash("invalid Login")
            return False
        if not bcrypt.check_password_hash(user.password, data["password"]):
            flash("invalid Login")
            return False

        return True

    @staticmethod
    def update_validator(data):
        is_valid = True
        if len(data["first_name"]) <= 2:
            flash("First Name must be at least 3 characters long")
            is_valid = False
        if len(data["last_name"]) <= 2:
            flash("Last Name must be at least 3 characters long")
            is_valid = False
        if len(data["email"]) <= 7:
            flash("email must be at least 8 characters long")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("please submit a valid email address")
            is_valid = False
        
        return is_valid

    
    @staticmethod
    def registry_validator(data):
        is_valid = True

        if len(data["first_name"]) <= 2:
            flash("First Name must be at least 3 characters long")
            is_valid = False
        if len(data["last_name"]) <= 2:
            flash("Last Name must be at least 3 characters long")
            is_valid = False
            
        user = User.get_by_email(data)
        if user:                            # <<<<-------------checks if email is already in use
            flash("email is already in use")
        
        if len(data["email"]) <= 7:
            flash("email must be at least 8 characters long")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("please submit a valid email address")
            is_valid = False

        if len(data["password"]) <= 7:
            flash("password must be at least 8 characters long")
            is_valid = False

        if data["password"] != data["confirm_password"]:
            flash("confirmed password must match password")
            is_valid = False

        return is_valid