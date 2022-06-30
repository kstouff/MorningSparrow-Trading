from flask import Flask
import requests
import pprint

url = "https://yh-finance.p.rapidapi.com/stock/v2/get-profile"




def check_company_data(symbol):
    
    querystring = {"symbol":f"{symbol}","region":"US"}

    headers = {
    	"X-RapidAPI-Host": "yh-finance.p.rapidapi.com",
    	"X-RapidAPI-Key": "bb895b25femsh0dd1a78a92b3d25p1f7653jsn6aaa727705ce"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    price = response.json().get('price').get('regularMarketPrice').get('raw')
    company_name = response.json().get('price').get('longName')

    result = {
        "price_per_share" : price, 
        "name" : company_name,
        }

    if price == None:  
        return print("no company found")
    return result

