from django.shortcuts import render
from .models import SheetInfo
from .utils.telegram_send import check_base_to_expire_date
from .utils.database_operations import write_to_base
# from .utils.main import sheet, sheet_id
# import asyncio
import threading


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
    
    check_base_to_expire_date(django_database)
    
    return render(request, 'sheets_app/index.html', {'database': django_database})


