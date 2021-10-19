#C:\Users\VIP\AppData\Local\Microsoft\WindowsApps\python3.9
from __future__ import print_function 
from datetime import date
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

socket.setdefaulttimeout(1200)  # set timeout to 10 minutes

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']




def main():
    """
    1. Authenticate
    2. Read keywords data
    3. Call Google Trends API for trends data
    """
    sheet = authenticate()
    
    # Read Keyword Input
    result = sheet.values().get(spreadsheetId=SPREADSHEET_URL,
                                range="keyword!A2:B").execute()
   
    # Call Google Trends API
    getTrendData(result.get('values'),GEO)




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

