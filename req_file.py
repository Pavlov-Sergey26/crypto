import os
from dotenv import load_dotenv, find_dotenv
import json, hmac, hashlib, time, base64
import requests
from datetime import datetime, timedelta
import datetime as DT  
import pymongo

def request_coinbase(url, endpoint):
    """Тут мы совершаем запросы в апи биржи"""

    #Считывание данных в приватном файле
    load_dotenv(find_dotenv())
    secretKey = os.environ.get("secretKey")
    access_key = os.environ.get("access_key")

    #Подключение к апи
    timestamp = str(int(time.time())) 
    payload = timestamp + "GET" + endpoint.split('?')[0]+""
    signature = hmac.new(secretKey.encode('utf-8'), payload.encode('utf-8'), digestmod=hashlib.sha256).digest()

    headers_coinbase = {
    'Content-Type': 'application/json',
    'CB-ACCESS-KEY': access_key, 
    'CB-ACCESS-SIGN':f'{signature.hex()}', 
    'CB-ACCESS-TIMESTAMP':f'{timestamp}'
    }

    req_coinbase = requests.get(url, headers=headers_coinbase).json()
    return req_coinbase


#Для практического задания 1 я взял недельный интервал и время просмотра 1 час(для примера)
futures = "ETH-USDT"
#Создаю переменны с временные отрезками в формате Unix
date_now = datetime.now()
date_now_minus7days = datetime.now() - timedelta(days=7)
dt_now = int(date_now.replace(tzinfo=DT.timezone.utc).timestamp())
dt_7days = int(date_now_minus7days.replace(tzinfo=DT.timezone.utc).timestamp())

url_candles = f"https://api.coinbase.com/api/v3/brokerage/products/{futures}/candles?start={dt_7days}&end={dt_now}&granularity=ONE_HOUR" #Для практического задания 1
url_price = f"https://api.coinbase.com/api/v3/brokerage/products/{futures}" #Для практического задания 2

#Вызов функции
request_coinbase_candles = request_coinbase(url_candles, f"/api/v3/brokerage/products/{futures}/candles") #Для практического задания 1
request_coinbase_price = request_coinbase(url_price, f"/api/v3/brokerage/products/{futures}") #Для практического задания 2


#Подключение базы данных MongoDB (Так же подключение и данные я сохранил в папке .env) #Для практического задания 2
load_dotenv(find_dotenv())
host = os.environ.get("host")
client = pymongo.MongoClient(host)
db = client.test1
coll = db.col_test

