from django.shortcuts import render
from .google.main import sheet, sheet_id
from models import SheetInfo

def index(request):
    django_database = SheetInfo.objects.all()
    
    try:
        sheet_base = sheet.values().get(spreadsheetId=sheet_id, range="Лист1").execute()
    
        for data in sheet_base['values'][1:]:
            if django_database.filter(id=data[0]):
                writeline = django_database.get(id=data[0])
                writeline.order_number=data[1]
                writeline.cost=data[2]
                writeline.delivery_time=data[3]
                writeline.cost_roubles=0
                writeline.save()
            else:
                django_database.create(id=data[0], order_number=data[1], cost=data[2], delivery_time=data[3], cost_roubles=0)
                
    except Exception as e2:
        print('Cant read from sheet_base in views.py:', e2)
        
    return render(request, 'sheets_app/index.html')