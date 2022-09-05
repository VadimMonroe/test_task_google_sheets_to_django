from datetime import datetime
from xmlrpc.client import _datetime_type

from telebot import TeleBot
import threading

# Эти данные должны быть в защищённом месте, для теста оставлю тут
TELEGRAM_BOT_TOKEN = '5323261089:AAHzX1L1M5q98t7xuicbUaJ58ouhfCLdb8Y'
TELEGRAM_CHAT_ID = '-1001742328980'
        
list_of_expired_dates = []

def get_expire_date(database: list[object], number: int, date_today: datetime) -> None:
    """
    Перебор проверки базы данных на просроченные даты.
    
        Параметры:
                    database (list[object]): Приходит список объектов из базы данных.
                    number (int): Порядковый номер перебора.
                    date_today datetime: Актуальная дата.
                    return (None): Ничего не возвращается.
    """
    global list_of_expired_dates
    
    cell_id = database.get(id=number)
    date_expire = datetime.strptime(cell_id.delivery_time , '%d.%m.%Y').date()
    if date_expire < date_today:
        list_of_expired_dates.append(f'🔴 Дата исполнения заказа id:{cell_id.id}: {date_expire} 🔴 Сегодняшняя дата: {date_today}')

def check_base_to_expire_date(database: list[object]) -> None:
    """
    Функция для проверки дат с истечением срока.
    
        Параметры:
                    database (list[object]): Приходит список объектов из базы данных.
                    return (None): Ничего не возвращается.
    """
    global list_of_expired_dates
    
    tasks = []
    date_today = datetime.today().date()
    
    for number in range(1, len(database)+1):
        # get_expire_date(database, number, date_today)
        tasks.append(threading.Thread(target=get_expire_date, args=(database, number, date_today)))
        tasks[number-1].start()
        
    [i.join() for i in tasks]

    send_telegram(list_of_expired_dates)
    tasks = []
    list_of_expired_dates = []

def send_telegram(list_of_expired_dates_inner: list) -> None:
    """
    Функция для отправки сообщения в телеграм.
    
        Параметры:
                    list_of_expired_dates (list): Приходит список просроченных id и дат.
                    return (None): Ничего не возвращается.
    """
    
    try:
        bot = TeleBot(token=TELEGRAM_BOT_TOKEN)
        toStroke = '\n'.join(list_of_expired_dates_inner)
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"{toStroke}", parse_mode='html')
    except Exception as e3:
        print('Cant send telegram message:', e3)