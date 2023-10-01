
import os
from Google import Create_Service
import gspread
import csv

FOLDER_PATH = 'C:/Users/sandi/Documents/'
CLIENT_SECRET_FILE = os.path.join(FOLDER_PATH, 'client_secret_317110996643-e4i4h3kp3nmpb19pradpmto1m5dhe29r.apps.googleusercontent.com.json')
API_SERVICE_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)

spreadsheet_id = "13k7aQPXNujk9hBH1SIO9-Ff_B1auPVGu_cbLNJew2H0"  # Please put your Spreadsheet ID.
sheet_name = "Sheet2"  
csv_file = "C:/Users/sandi/Downloads/biostats.csv"  # Please put the file path of the CSV file you want to use.

f = open(csv_file, "r")
values = [r for r in csv.reader(f)]
request = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=sheet_name, valueInputOption="USER_ENTERED", body={"values": values}).execute()