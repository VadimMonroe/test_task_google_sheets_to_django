import os
import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

sheet_id = '1EqvGMD5mpAmT0psvIlfzw7fBDWnzyrHaxCX6fX9i2jE'

def get_service_sacc() -> object:
    """
    Могу читать и (возможно) писать в таблицы, которой выдан доступ для сервисного аккаунта приложения
    :return:
    """
    
    creds_json = os.path.dirname(__file__) + "/digital-heading-361313-6bab50b1bd17.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
    return build('sheets', 'v4', http=creds_service)


service = get_service_sacc()
sheet = service.spreadsheets()

try:
    resp = sheet.values().get(spreadsheetId=sheet_id, range="Лист1").execute()
    for i in resp['values'][1:]:
        print(i)
except Exception as e:
    print('e', e)
    
# resp = ['1', '1249708', '675', '24.05.2022'], ['2', '1182407', '214', '13.05.2022']
