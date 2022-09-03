from django.shortcuts import render

def index(request):
    return render(request, 'sheets_app/index.html')