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

try:
    service = get_service_sacc()
    sheet = service.spreadsheets()
except Exception as e1:
    print('Error with service or sheet in main.py:', e1)
    
# resp = ['1', '1249708', '675', '24.05.2022'], ['2', '1182407', '214', '13.05.2022']
