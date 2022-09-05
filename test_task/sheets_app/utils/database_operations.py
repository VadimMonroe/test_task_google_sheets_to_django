from ..models import SheetInfo
from ..utils.usd_to_rub import roubles_from_usd
from .get_sheets import get_sheet_base
import threading

def write_to_base(data: list, number: int) -> None:
    """
    Функция для заполнения базы данных.
    
        Параметры:
                    data (list): Источником информации является список из значений одной строчки, пришешей из google sheets.
                    number (int): Номер строки из google sheets.
                    return (None) : Не возвращает ничего.
    """
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
            
# sheet_base = ['1', '1249708', '675', '24.05.2022'], ['2', '1182407', '214', '13.05.2022'], ['1', '1249708', '675', '24.05.2022'], ['2', '1182407', '214', '13.05.2022']

tasks = []
sheet_base_old = None
restrictions_per_minute = 60

def asynchronous_database() -> None:
    """
    Функция для запроса обновления данных с google sheets. 
    Если данные поменялись, обновляются в базе данных.
    
        Параметры:
                    return (None) : Не возвращает ничего.
    """
    global tasks, sheet_base_old, restrictions_per_minute
    
    
    sheet_base = get_sheet_base()
    
    if sheet_base != sheet_base_old:
        sheet_base_old = sheet_base
        try:
            
            for number, data in enumerate(sheet_base, start=1):
                tasks.append(threading.Thread(target=write_to_base, args=(data, number), daemon=False))
                tasks[number-1].start()
                
            [i.join() for i in tasks]
            tasks = []
                
        except Exception as e2:
            print('Cant read from sheet_base in views.py:', e2)