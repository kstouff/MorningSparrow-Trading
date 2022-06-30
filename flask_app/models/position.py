

from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import order


class Position:
    def __init__(self, data) -> None:
        self.id = data["id"]
        self.value = data["value"]
        self.account_id = data["account_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.companies = []

    @classmethod
    def get_position_by_company(cls):
        
        mysql = connectToMySQL("trading_test")
        query = "Select * From companies join orders on company_id = companies.id;"
        results = mysql.query_db(query)
        all_positions = []
        if results:
            for row in results:
                all_positions.append(row)
            return all_positions
        if not results:
            return False

    @classmethod
    def check_if_already_position(cls, data):
        positions = Position.get_position_by_company()
        for row in positions:
            if row['companies.id'] == data["company.id"]:
                print("position already exisits")
            else:
                print("time to create a new positon")

    @classmethod
    def create_position(cls, data):
        mysql = connectToMySQL('trading_test')
        query = "INSERT INTO positions (value, account_id) values(0, %(account_id)s)"
        mysql.query_db(query, data)

    @classmethod
    def show_all_by_account(cls, data):
        mysql = connectToMySQL('trading_test')
        query = "SELECT * FROM positions join orders on position_id = positions.id join companies on company_id = companies.id WHERE account_id = %(account_id)s;"
        results = mysql.query_db(query, data)
        all_positions = []
        if results:
            for row in results:

                all_positions.append(row)
            return all_positions


