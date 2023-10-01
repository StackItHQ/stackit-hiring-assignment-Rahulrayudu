import os
from Google import Create_Service
import pandas as pd
import numpy as np

FOLDER_PATH = 'C:/Users/sandi/Documents/'
CLIENT_SECRET_FILE = os.path.join(FOLDER_PATH, 'client_secret_317110996643-e4i4h3kp3nmpb19pradpmto1m5dhe29r.apps.googleusercontent.com.json')
API_SERVICE_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SPREADSHEET_ID = '13k7aQPXNujk9hBH1SIO9-Ff_B1auPVGu_cbLNJew2H0'

# creating the service instance
service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)

# exporting csv as dataframe

def export_data_to_sheets():
    URL = r'https://people.sc.fsu.edu/~jburkardt/data/csv/biostats.csv'
    df = pd.read_csv(URL)
    df.replace(np.nan, '', inplace=True)
    i=0
    for col in df.columns:
        print(f"{i}: {col}")
        i+=1

    # giving user option for column selection

    selected_columns = input("Enter the column numbers (comma-separated) you want to Keep: ")
    selected_column_indices = [int(idx) for idx in selected_columns.split(",")]
    print(selected_column_indices)
    df = df.iloc[:, selected_column_indices]
    response = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        valueInputOption='RAW',
        range='Sheet1',
        body=dict(
            majorDimension='ROWS',
            values=df.T.reset_index().T.values.tolist())
    ).execute()

export_data_to_sheets()
