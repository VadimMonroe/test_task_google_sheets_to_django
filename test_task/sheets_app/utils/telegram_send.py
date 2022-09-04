from datetime import datetime

from telebot import TeleBot

# Эти данные должны быть в защищённом месте, для теста оставлю тут
TELEGRAM_BOT_TOKEN = '5245977303:AAEdPfBqPjllawUskZfbo7v6YU0NOWpiwlg'
TELEGRAM_CHAT_ID = '-1001732100302'
        
def check_base_to_expire_date(database: list[object]) -> None:
    """
    Функция для проверки дат с истечением срока.
    
        Параметры:
                    database: (list[object]): Приходит список объектов из базы данных.
                    return (None): Ничего не возвращается.
    """
    
    date_today = datetime.today().date()
    list_of_expired_dates = []
    
    for number in range(1, len(database)+1):
        cell_id = database.get(id=number)
        date_expire = datetime.strptime(cell_id.delivery_time , '%d.%m.%Y').date()
        if date_expire < date_today:
            list_of_expired_dates.append(f'🔴 Дата исполнения заказа id:{cell_id.id}: {date_expire} 🔴 Сегодняшняя дата: {date_today}')
        
    send_telegram(list_of_expired_dates)

def send_telegram(list_of_expired_dates: list) -> None:
    """
    Функция для отправки сообщения в телеграм.
    
        Параметры:
                    list_of_expired_dates (list): Приходит список просроченных id и дат.
                    return (None): Ничего не возвращается.
    """
    
    try:
        bot = TeleBot(token=TELEGRAM_BOT_TOKEN)
        toStroke = '\n'.join(list_of_expired_dates)
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"{toStroke}", parse_mode='html')
    except Exception as e3:
        print('Cant send telegram message:', e3)