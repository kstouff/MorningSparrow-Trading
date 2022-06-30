from flask import session
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import company
from flask_app.models import order
from flask_app.models import user

class Account:
    def __init__(self, data) -> None:
        self.id = data["id"]
        self.name = data["name"]
        self.value = data["value"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

        self.company = []


    @classmethod
    def create(cls, data):
        mysql = connectToMySQL("trading_test")
        query = "INSERT INTO accounts (name, value, user_id) Values(%(name)s, %(value)s, %(user_id)s);"
        mysql.query_db(query, data)
        return

    @classmethod
    def delete(cls, data):
        mysql = connectToMySQL("trading_test")
        query = "DELETE FROM accounts WHERE id = %(id)s;"
        mysql.query_db(query, data)
        return

    @classmethod
    def get_accounts(cls, data):
        mysql = connectToMySQL("trading_test")
        query = "SELECT * FROM accounts WHERE id = %(id)s;"
        results = mysql.query_db(query, data)
        return cls(results)

    @classmethod
    def get_with_order_totals(cls, data):
        query = "Select accounts.*, companies.*,  sum(orders.share_num) as total_shares, sum(orders.share_num * companies.price_per_share) as total_value, avg(orders.price_per_share) as average_price from accounts join orders on accounts.id = account_id join companies on company_id = companies.id where accounts.id = %(id)s group by company_id;"
        mysql = connectToMySQL('trading_test')
        results = mysql.query_db(query, data)
        all_accounts = []
        if results:
            for row in results:
                temp_account = cls(row)
                company_data = {
                    "id" : row["companies.id"],
                    "name" : row["companies.name"],
                    "share_num" : row["share_num"],
                    "price_per_share" : row["price_per_share"],
                    "num_shares_outstanding" : row["num_shares_outstanding"],
                    "created_at" : row["companies.created_at"],
                    "updated_at" : row["companies.updated_at"]
                }
                total_shares = row['total_shares']
                total_value = row['total_value']
                average_price = row['average_price']
                temp_account.company = company.Company(company_data)
                temp_account.total_shares = total_shares
                temp_account.total_value = total_value
                temp_account.average_price = average_price

                all_accounts.append(temp_account)
        return all_accounts
                


    @classmethod
    def get_account_with_companies(cls, data):
    
        mysql = connectToMySQL("trading_test")
        query = "Select * From accounts left join orders on accounts.id = account_id left join companies on company_id = companies.id WHERE accounts.id = %(id)s;"
        results = mysql.query_db(query, data)
        account = cls(results[0])
        for row in results:
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
                "updated_at" : row["companies.updated_at"],
                "position_id" : row["companies.position_id"]
            } 
            account.companies.append(company.Company(company_data))    
            account.orders.append(order.Order(order_data))    
        return account       



    @classmethod
    def deposit(cls, data):
        # accounts = user.User.get_user_with_accounts({"id" : session['user_id']}) 
        # for account in accounts:
        #     print(account.id, account.name, data['id'])
        #     print(data)
        #     if int(account.id) == int(data['id']):
        #         print("success")
        #         cash_balance = int(account.value)
        #         cash_balance += int(data['deposit'])
        #         data['cash_balance'] = cash_balance

        mysql = connectToMySQL("trading_test")
        query = "UPDATE accounts SET value = value + %(deposit)s WHERE id = %(id)s"
        mysql.query_db(query, data)

    @classmethod
    def withdraw(cls, data):
        # print(data)
        # accounts = user.User.get_user_with_accounts({"id" : session['user_id']}) 
        # for account in accounts:
        #     print(account.id, account.name)
        #     if int(account.id) == int(data['id']):
        #         cash_balance = int(account.value)
        #         cash_balance -= int(data['withdraw'])
        #         data['cash_balance'] = cash_balance
        #         print(data)

        mysql = connectToMySQL("trading_test")
        query = "UPDATE accounts SET value = value - %(withdraw)s WHERE id = %(id)s"
        mysql.query_db(query, data)

