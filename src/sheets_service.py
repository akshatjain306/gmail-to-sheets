from googleapiclient.discovery import build
from gmail_service import get_gmail_service

def get_sheets_service():
    creds = get_gmail_service()._http.credentials
    return build('sheets', 'v4', credentials=creds)

def append_row(sheet_id, row):
    service = get_sheets_service()
    body = {'values': [row]}

    service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range='Sheet1!A1',
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()
