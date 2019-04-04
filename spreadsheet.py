# A class with functions to interact with google sheets.
# Used for headless testing in the Jenkins-BitBucket pipeline.
# Uses a private key to have edit access to sheets.
# Be careful to avoid logging sensitive data.

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import base64

# Code that is not made into a function runs automatically upon import.
class Spreadsheet:

    def __init__(self):
        # Use creds to create a client to interact with the Google Drive API
        scope = ['https://www.googleapis.com/auth/drive'] # 'https://www.googleapis.com/auth/spreadsheets', 'https://spreadsheets.google.com/feeds'
        self.client = None
        self.sheet = None
        with open('secret.json', 'rb') as f:
            x = base64.b64decode(f.read()) # decode creds
            with open('temp.json', 'wb') as f:
                f.write(x)
            creds = ServiceAccountCredentials.from_json_keyfile_name('temp.json', scope)
            self.client = gspread.authorize(creds)

    def __del__(self):
        if self.client is not None:
            self.client = None
        with open('temp.json', 'wb') as f:
            f.write(b'')

    # Class functions modify the Spreadsheet object, and often don't return values.
    # Find a workbook by name and open the first sheet.
    # TODO: make this part more generic??
    def open_sheet(self, testname):
        if testname=="ChesProdTitleTest":
            self.sheet = self.client.open("Headless Test Results").get_worksheet(0)
        elif testname=="LampDevTest":
            self.sheet = self.client.open("Headless Test Results").get_worksheet(1)
        elif testname=="IdmCampusDirectoryTest":
            self.sheet = self.client.open("Headless Test Results").get_worksheet(2)
        else:
            # create a new worksheet in your spreadsheet
            spreadsheet = self.client.open("Headless Test Results")
            self.sheet = spreadsheet.add_worksheet(title=testname, rows="500", cols="20")

    # Log the test result
    def write_cell(self, row, col, msg):
        # sheet.clear()
        # Extract all of the values
        # list_of_sites = sheet.get_all_values()
        # syntax: update_cell(row, column, value to insert)
        self.sheet.update_cell(row, col, msg)


    # Find next available column TODO need to update this
    def next_available_row(self):
        if self.sheet is None:
            print("You need to open the sheet before trying to get values")
            return
        # last_col = len(worksheet.row_values(1)) # number of values in the row
        #TODO: find a faster way. The runtime of this gets slower as more data is appended
        return len(self.sheet.get_all_values()) + 2 # next row to write into
