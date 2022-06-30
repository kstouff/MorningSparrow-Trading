from flask import session
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app.models import position

class Order:
    def __init__(self, data) -> None:
        self.id = data["id"]
        self.share_num = data["share_num"]
        self.price_per_share = data["price_per_share"]
        self.company_id = data["company_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.account_id = data["account_id"]

    @classmethod
    def calculate_purachase(cls, shares, price):
        total = int(shares) * int(price)
        return total

    @classmethod
    def get_order():
        query = 'select * from orders Where id = '
        pass


    @classmethod
    def create_order(cls, data):

        mysql = connectToMySQL('trading_test')
        query = "INSERT INTO orders (share_num, price_per_share, company_id, account_id) VALUES(%(share_num)s, %(price_per_share)s, %(company_id)s, %(account_id)s); "
        mysql.query_db(query, data)



