from flask_app import app
from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL

class Company:
    def __init__(self, data) -> None:
        self.id = data["id"]
        self.name = data["name"]
        self.share_num = data["share_num"]
        self.price_per_share = data["price_per_share"]
        self.num_shares_outstanding = data["num_shares_outstanding"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.accounts = []






    @classmethod
    def delete(cls, data):
        query = "DELETE FROM companies WHERE id = %(id)s"
        connectToMySQL("trading_test").query_db(query, data)
    
    @classmethod
    def get_all_companies(cls):
        mysql = connectToMySQL("trading_test")
        query = "SELECT * FROM companies;"
        results = mysql.query_db(query)
        all_companies = []
        if results:
            for row in results:
                all_companies.append(cls(row)) 
        return all_companies

    @classmethod
    def Update_outstanding_shares(cls, data):
        query = "UPDATE companies SET num_shares_outstanding = %(num_shares_outstanding)s WHERE id = %(id)s"
        connectToMySQL("trading_test").query_db(query, data)

    @classmethod
    def Update_company_prices(cls, data):
        query = "UPDATE companies SET price_per_share = %(price_per_share)s WHERE id = %(id)s"
        connectToMySQL("trading_test").query_db(query, data)

    @classmethod
    def get_company(cls, data):
        mysql = connectToMySQL("trading_test")
        query = "SELECT * FROM companies WHERE id = %(id)s;"
        results = mysql.query_db(query, data)
        print(results)
        if results:
            return cls(results[0])

    @classmethod
    def caculate_updated_outstanding_shares(cls, company_id, num_shares):
        company = Company.get_company({"id" : company_id})
        print(company)
        print(("*")*100)
        current_oustanding_shares = int(company.num_shares_outstanding)
        current_oustanding_shares -= int(num_shares)
        data = {
            "id" : company_id,
            "num_shares_outstanding" : current_oustanding_shares
        }
        Company.Update_outstanding_shares(data)



    @classmethod
    def create_one(cls, data):
        
        mysql = connectToMySQL("trading_test")
        query = "Insert Into companies (name, share_num, price_per_share, num_shares_outstanding) Values(%(name)s, 100000, %(price_per_share)s, 100000);"
        return mysql.query_db(query, data)

