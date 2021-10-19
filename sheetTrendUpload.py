#C:\Users\VIP\AppData\Local\Microsoft\WindowsApps\python3.9
from __future__ import print_function 
from trend import *
from datetime import datetime,date
import pickle
import os.path
from googleapiclient import discovery
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests
import socket
import sys, errno

socket.setdefaulttimeout(1200)  # set timeout to 10 minutes

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']



def main():
    """
    1. Authenticate
    2. Push trend data to sheet
    3. Update New Title
    """
    # Authenticate
    sheet = authenticate()

    # Push data trends to sheet
    tabName = "data trend!A:D"
    sheet.values().clear(spreadsheetId=SPREADSHEET_URL, range=tabName).execute()
    values = readCSV(CLIENT_NAME+'-'+GEO+'.csv')
    value_input_option = "USER_ENTERED"
    body = {

        'values': values
    }

    result = sheet.values().update(
        spreadsheetId=SPREADSHEET_URL, range=tabName,
        valueInputOption=value_input_option, body=body).execute()

    # Update New Title
    updateNewTitle(sheet)




def updateNewTitle(sheet):
    # Update New Title
    today = date.today()
    newName = CLIENT_NAME +" // Google Trends " + today.strftime("%d%m%Y")
    body = {
        "requests": { 
            "updateSpreadsheetProperties" : {
                "fields" : "title",
                "properties" : {
                    "title" : newName
                }
            }
        }
    }
    sheet.batchUpdate(spreadsheetId=SPREADSHEET_URL, body=body).execute()







def authenticate():
    """
    Authentication Starts
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

