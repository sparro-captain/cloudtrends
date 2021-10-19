#C:\Users\VIP\AppData\Local\Microsoft\WindowsApps\python3.9
from __future__ import print_function 
from trend import *
from datetime import datetime
import pickle
import os.path
from googleapiclient import discovery
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests
import socket
import sys, errno
from datetime import date, datetime

socket.setdefaulttimeout(1200)  # set timeout to 10 minutes

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def main():
    """
        1. Authenticate
        2. Read keywords from Sheet
        3. Call Google Trends API for Related Queries data
        4. Write related queries data to Sheet
    """
    #   Authenticate
    sheet = authenticate()

    # Read Keyword Input
    result = sheet.values().get(spreadsheetId=SPREADSHEET_URL,
                                range="keyword!C2:C").execute()
    
    # Call Google Trends API
    getRelatedData(result.get('values'),GEO)


    # Push data to sheet
    tabName = "data topOrRising!A:D"
    sheet.values().clear(spreadsheetId=SPREADSHEET_URL, range=tabName).execute()
    values = readCSV(CLIENT_NAME+'-'+GEO+'-TopOrRising.csv')
    value_input_option = "USER_ENTERED"
    body = {
        'values': values
    }

    result = sheet.values().update(
        spreadsheetId=SPREADSHEET_URL, range=tabName,
        valueInputOption=value_input_option, body=body).execute()















def authenticate():
    """
    Authentication starts
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
    
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('sheets', 'v4', credentials=creds)
    return service.spreadsheets()

if __name__ == "__main__":
    main()

