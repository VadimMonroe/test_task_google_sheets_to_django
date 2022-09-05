import os
import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

sheet_id = '1EqvGMD5mpAmT0psvIlfzw7fBDWnzyrHaxCX6fX9i2jE'

def get_service_sacc() -> object:
    """
    Функция считывающая информацию с таблицы google sheets, которой выдан доступ для сервисного аккаунта приложения.
        
        Параметры:
                    return (None) : Возвращает объект из которого считываются данные.
    """
    
    creds_json = os.path.dirname(__file__) + "/digital-heading-361313-6bab50b1bd17.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
        
    return build('sheets', 'v4', http=creds_service)


service = get_service_sacc()
sheet = service.spreadsheets()

def get_sheet_base() -> list[list]:
    """
    Функция для запроса данных из google sheets.
    При получении данных считываются в список списков.
    
        Параметры:
                    return (None) : Список списков строк.
    """

    try:
        sheet_base = sheet.values().get(spreadsheetId=sheet_id, range="Лист1").execute()['values'][1:]
    except Exception as e7:
        print('Cant take sheets:', e7)
        
    return sheet_base