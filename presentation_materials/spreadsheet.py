import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import basic_test


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Selenium Testing - Input and Output").get_worksheet(0)
results = client.open("Selenium Testing - Input and Output").get_worksheet(1)
results.clear()

# Extract and print all of the values
list_of_sites = sheet.get_all_values()

i = 1

for site in list_of_sites:
    if site[0] != 'URL':

        # Create a new instance of the Firefox driver
        driver = webdriver.Firefox()


        basic_result = basic_test.basic_test(driver,results,site[0],i)

        #run advanced test if basic passed and advanced test requested
        if ((basic_result == 0) and (site[1] == 'y')):
            #to-do define what an advanced test looks like and how results are documented
            advanced_result = 1

        i=i+1
        driver.quit()

