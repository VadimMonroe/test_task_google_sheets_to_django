from django.shortcuts import render
from .models import SheetInfo
from .utils.telegram_send import check_base_to_expire_date
from .utils.database_operations import asynchronous_database

         
def index(request):
    asynchronous_database()
    
    django_database = SheetInfo.objects.all().order_by('id')
    check_base_to_expire_date(django_database)
    
    return render(request, 'sheets_app/index.html', {'database': django_database})


