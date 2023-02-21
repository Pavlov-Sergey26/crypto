#Добрый день, выполнил тестовое задание, тут немного расскажу, что выполнил
#Работаю через репозиторий гита, сделал файл .env c помощью пакета dotenv, 
#Который скрывает данные от апи  (чтобы не показывать их в публичном доступе)
#Решил подключить апи биржи coinbase
#Немного о моих навыках, я уже работал и работаю с приложениями по финансовым рынкам
#И крипте, приложения созданы для компании (не пет проекты), с радостью бы показал свои наработки в этой сфере


#TODO Чтобы не засорять весь маин файл запросы будут проводиться в файле req_file, так лаконичнее и приятнее глазу
from req_file import request_coinbase_candles, request_coinbase_price, coll, requests
from datetime import datetime, timedelta
import calendar, time

#Практическое 1
#Определить собственные движения цены фьючерса ETHUSDT
#Я выбрал методику отслеживания крипто-биржи (на данный момент "Coinbase", но можно любую)
#В качестве параметров я взял данные по изменению цены фьючерса и дату в момент изменения цены

#TODO Так как словарь выдается в обратном порядке (сначала нынешнее число, а потом недельной давности),
#То я развернул словарь (так удобнее работать)
time_for_price = []
price = []
for find_info in reversed(request_coinbase_candles['candles']):
    time_for_price.append(find_info['start'])
    price.append(find_info['high'])

#Данные вытащили, теперь мы можем работать с ними, к примеру этот список мы можем закинуть в базу данных или же создать график в реальном времени


#Практическое 2
#Программа в реальном времени отслеживет крипто-биржу "Coinbase" и следит за ценой фьючерса ETHUSDT
#Для того чтобы программа работала в автоматическом режиме, предлагаю воспользоваться cron
#Вот путь для срабатывания cron 1 * * * * /path/crypto/venv/Script/activate /path/crypto/main_file.py
#На данный момент cron работает каждые 60 минут или час

def find_price_for_futures(req):
    """Функция отслеживает цену фьючерса и изменения цены в процентах
    Чтобы отслеживать изменение цены предлагаю подключить базу данных
    Для работы я взял MongoDB, алгоритм будет такой:
    Мы сохраняем в базу данных два значения индексированное значение время (pk) и нынешний процент
    Дальше мы делаем запрос, вытащи нам данные по pk, который равен время сейчас - 60 минут и 
    Сравни, изменился ли процент за это время, если да, то выводи в консоль сообщение"""

    date_now = datetime.now()
    price_now = float(req['price'])
    percent_now = float(req['price_percentage_change_24h'])
    #Загружаю данные в бд
    insert = { '_id':f'{str(date_now)[:13]}',
            'percent': percent_now}
    coll.insert_one(insert)
    
    #Вытаскиваю данные из бд
    check_percent = coll.find({ '_id':f"{(date_now - timedelta(hours=1)).strftime('%Y-%m-%d %H')}"})
    for check in check_percent:
        if percent_now > (float(check['percent'])+1) or percent_now < (float(check['percent'])-1):
            print(f"За последний час цена фьючерса ETH-USDT изменилась с {percent_now:.{2}f}% на {check['percent']:.{2}f}% ")

            #Решил cделать бонусом, выводить "логи" в какой нибудь чат, для примера я взял Discord
            header_dis = {'authorization': 'MzM1ODI5NDEwNzYwNjIyMDgw.GCAfrU.IspLu7FBf1gfKcnmuWs32eWeKxc0nXr2UedeEA'}
            dis_req = requests.post(url='https://discord.com/api/v9/channels/1006914263207649371/messages', data={'content':f"За последний час цена фьючерса ETH-USDT изменилась с {percent_now:.{2}f}% на {check['percent']:.{2}f}% "}, headers=header_dis)
    #Вывод тестов: За последний час цена фьючерса ETH-USDT изменилась с -1.67% на -0.63% 


find_price_for_futures(request_coinbase_price)
