import os
from datetime import datetime, timedelta
import json
import requests
import lxml

from bs4 import BeautifulSoup

def roubles_from_usd(usd: str) -> int:
    """
    Функция для получения курса ЦБ РФ.
    
        Параметры:
                    usd (str): Приходит параметр usd в строковом формате.
                    return : Возвращает значение USD * на курс USD.
        
        Функционал:
                    1. Исключаются какие-либо рассчёты, если usd равен 0.
                    2. Т.к. у сайта XML_daily.asp ограниченное кол-во запросов в день,
                        записываем значение курса USD в файл usd_exchange.json и используем до завершения дня.
    """
    usd = float(usd)
    
    if usd == 0:
        return usd
    
    file_path = os.path.dirname(__file__) + '/usd_exchange.json'
    date_today = str((datetime.now() + timedelta(days=-1)).date())
    
    with open (file_path, 'r') as f:
        info = json.load(f)
    
    if info["date"] != date_today:
        try:
            response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp')
            dom = BeautifulSoup(response.text, 'xml')
            # actual_date = dom.find('ValCurs').Date.text
            # print(actual_date)
            usd_exchange = float(dom.find(ID='R01235').Value.text.replace(',', '.')) if usd != 0 else 0
        except Exception as e4:
            print('Не могу извлечь информацию из сайта https://www.cbr.ru/scripts/XML_daily.asp', e4)
            usd_exchange = 60
            
        with open (file_path, 'w') as f:
            new_info = {"date": date_today, "usd": usd_exchange}
            json.dump(new_info, f)
    else:
        usd_exchange = info["usd"]
    
    result = usd * usd_exchange
    return int(result)