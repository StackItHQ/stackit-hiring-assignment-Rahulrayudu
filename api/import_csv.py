import streamlit as st
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


def main():
    st.subheader("StockIt Please Upload the CSV file")
    data = st.file_uploader("Upload a Dataset", type=["csv", "txt"])


    if data is not None:
        df = pd.read_csv(data)
        st.dataframe(df.head())

        # Allow the user to select columns
        st.subheader("Select the Columns")
        selected_columns = st.multiselect("Select Columns", df.columns.tolist())
        if selected_columns:
            new_df = df[selected_columns]
            st.dataframe(new_df.head())
            df = new_df

        st.subheader("Filter Option")
        selec_column = st.selectbox("Select Columns for Filter", df.columns.tolist())
        if selec_column:
            # Infer the data type of the selected column
            column_dtype = df[selec_column].dtype

            filter_options = ["None"]  # Default option

            if column_dtype == 'int64' or column_dtype == 'float64':
                filter_options.extend(["Equal to", "Less than", "Greater than"])
            elif column_dtype == 'object':  # String column
                filter_options.extend(["Equal to", "Contains", "Starts with", "Ends with"])

            filter_option = st.selectbox("Filter Option", filter_options)

            if filter_option != "None":
                # Get the filter value from the user
                filter_value = st.text_input("Filter Value", "")
                if filter_value:
                    # Convert the filter_value to the appropriate data type
                    if column_dtype == 'int64':
                        filter_value = int(filter_value)
                    elif column_dtype == 'float64':
                        filter_value = float(filter_value)

                    if column_dtype == 'object':  # String column
                        if filter_option == "Equal to":
                            new_df1 = df[df[selec_column] == filter_value]
                        elif filter_option == "Contains":
                            new_df1 = df[df[selec_column].str.contains(filter_value)]
                        elif filter_option == "Starts with":
                            new_df1 = df[df[selec_column].str.startswith(filter_value)]
                        elif filter_option == "Ends with":
                            new_df1 = df[df[selec_column].str.endswith(filter_value)]
                    else:  # Numeric columns
                        if filter_option == "Equal to":
                            new_df1 = df[df[selec_column] == filter_value]
                        elif filter_option == "Less than":
                            new_df1 = df[df[selec_column] < filter_value]
                        elif filter_option == "Greater than":
                            new_df1 = df[df[selec_column] > filter_value]

                    st.dataframe(new_df1.head())
                    st.write(column_dtype)
                    if st.button("Apply Filter"):
                        response = service.spreadsheets().values().append(
                            spreadsheetId=SPREADSHEET_ID,
                            valueInputOption='RAW',
                            range='Sheet1',
                            body=dict(
                                majorDimension='ROWS',
                                values=new_df1.T.reset_index().T.values.tolist())
                        ).execute()



if __name__ == '__main__':
    main()
