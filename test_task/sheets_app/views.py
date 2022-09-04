from django.shortcuts import render
# from .google.main import sheet, sheet_id
from .models import SheetInfo
# import asyncio
import threading
import requests
from bs4 import BeautifulSoup
import lxml
from datetime import datetime
from telebot import TeleBot, types

def write_to_base(data, number):
    django_database = SheetInfo.objects.all()
    
    if data:
        if django_database.filter(id=data[0]):
            writeline = django_database.get(id=data[0]) if 0 < len(data) else django_database.filter(id=number)
            if [str(writeline.id), str(writeline.order_number), str(writeline.cost), writeline.delivery_time] != data:
                writeline.order_number = data[1] if 1 < len(data) else 0
                writeline.cost = data[2] if 2 < len(data) else 0
                writeline.delivery_time=data[3] if 3 < len(data) else '0'
                writeline.cost_roubles = roubles_from_usd(writeline.cost)
                writeline.save()
            
            if writeline.cost_roubles != roubles_from_usd(data[2]):
                writeline.cost = data[2] if 2 < len(data) else 0
                writeline.cost_roubles = roubles_from_usd(writeline.cost)
                writeline.save()
        else:
            django_database.create(id=data[0], order_number=data[1], cost=data[2], delivery_time=data[3], cost_roubles=roubles_from_usd(data[2]))
    else:
        if django_database.filter(id=number):
            writeline = django_database.get(id=number)
            writeline.order_number = 0
            writeline.cost = 0
            writeline.delivery_time = '0'
            writeline.cost_roubles = 0
            writeline.save()
        else:
            django_database.create(id=number, order_number=0, cost=0, delivery_time='0', cost_roubles=0)
    

def index(request):
    tasks =[]
    
    try:
        # sheet_base = sheet.values().get(spreadsheetId=sheet_id, range="Лист1").execute()
        # for number, data in enumerate(sheet_base['values'][1:], start=1):
        sheet_base = ['1', '1249708', '675', '24.05.2022'], ['2', '1182407', '214', '13.05.2022'], ['1', '1249708', '675', '24.05.2022'], ['2', '1182407', '214', '13.05.2022']
        for number, data in enumerate(sheet_base, start=1):

            # asyncio.run(write_to_base(data, number))
            task = threading.Thread(target=write_to_base, args=(data, number), daemon=False)
            task.start()
            tasks.append(task)
    except Exception as e2:
        print('Cant read from sheet_base in views.py:', e2)
        
    # for i in tasks:
    #     i.join()
    
    django_database = SheetInfo.objects.all().order_by('id')
    check_date_to_send_telegram(django_database.filter(id=data[0]).get(id=data[0]).id, 
                                django_database.filter(id=data[0]).get(id=data[0]).delivery_time)
    
    return render(request, 'sheets_app/index.html', {'database': django_database})

def roubles_from_usd(usd):
    response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp')
    dom = BeautifulSoup(response.text, 'xml')
    usd = float(usd)
    result = usd * float(dom.find(ID='R01235').Value.text.replace(',', '.')) if usd != 0 else 0
    return int(result)

def check_date_to_send_telegram(id, date):
    date_expire = datetime.strptime(date, '%d.%m.%Y').date()
    date_today = datetime.today().date()
    
    if date_expire < date_today:
        list_of_something = [f'Дата исполнения заказа {id}: {date_expire}', f'Сегодняшняя дата: {date_today}']
        
        TELEGRAM_BOT_TOKEN = '5245977303:AAEdPfBqPjllawUskZfbo7v6YU0NOWpiwlg'
        TELEGRAM_CHAT_ID = '-1001732100302'
        
        try:
            bot = TeleBot(token=TELEGRAM_BOT_TOKEN)
            toStroke = '\n'.join(list_of_something)
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"{toStroke}", parse_mode='html')
        except Exception as e3:
            print('Cant send telegram message:', e3)