#!/usr/local/bin/python
# coding=utf-8

# Headless firefox title test for jenkins build.

intro="""
----------------------------------------------------------------
File        : ches_prod_test_titles_headless.py
Description : Headless firefox title test for ches prod sites.
Author      : Sherri Li
----------------------------------------------------------------
"""
print(intro)

from selenium import webdriver
from xvfbwrapper import Xvfb
import unittest
import os
import sys
sys.path.append("..")
import json
import time
import datetime
import timeit
import logging
import write_log
import check_status
import create_log
import spreadsheet


# Generate log folder and file.
# Default log level is INFO (everything). Go to create_log.py to change.
folderName = create_log.createLog("ChesProdTitle")

class ChesProdTitleTest(unittest.TestCase):
    # Name of the JSON file containing the sites to test
    json_file = "sites-prod.json" # can modify later
    today = str(datetime.datetime.now())
    # Here are the class variables shared among all instances "self" of ChesProdTitleTest
    ERRORCOLOR = "\u001b[31m" #red
    WARNINGCOLOR = "\u001b[33m" #yellow
    SUCCESSCOLOR = "\u001b[32m" #green
    DEFAULTCOLOR = "\u001b[0m" #white
    browser = None
    browserType = 'firefox'
    sites = None
    timeStart = None


###################################
# SETUP FUNCTIONS #################
###################################
    def __init__(self, *args, **kwargs):
        super(ChesProdTitleTest, self).__init__(*args, **kwargs)
        if self.sites is None:
            self.setupSites()
        # Initialize a Spreadsheet object!
        self.spreadsheet = spreadsheet.Spreadsheet()
        self.spreadsheet.open_sheet(str(type(self).__name__))
        self.next_row = self.spreadsheet.next_available_row()

    def __del__(self):
        if self.browser is not None:
            try:
                self.browser.quit()
            except:
                pass
        try:
            del self.spreadsheet
        except Exception as e:
            print(e)

# NOTE: timer integrated into helper function to making gspread logging easier.

    # def setUp(self):
    #     if self.timeStart is None:
    #         self.timeStart = timeit.default_timer()
    #
    # def tearDown(self):
    #     if self.timeStart is not None:
    #         timeElapsed = timeit.default_timer() - self.timeStart
    #         write_log.logSummary(self.browserType, timeElapsed)

    def setupSites(self):
        #use json credentials file
        with open(os.getcwd() + '/' + self.json_file) as data_file:
            data = json.load(data_file)
            self.sites = {}
            for siteData in data['sites']:
                site = {}
                site['url']= siteData['url']
                site['title']= siteData['title']
                self.sites[siteData['siteName']] = site


###################################
# TEST FUNCTIONS ##################
###################################
    # def test_admissions(self):
    #     self.run_test('admissions', self.next_row)
    #
    # def test_admstats(self):
    #     self.run_test("admstats", self.next_row+1)
    #
    # def test_btconference(self):
    #     self.run_test("btconference", self.next_row+2)
    #
    # def test_conrooms(self):
    #     self.run_test("conrooms", self.next_row+3)
    #
    # def test_careercentersecure_student(self):
    #     self.run_test("careercentersecure-student", self.next_row+4)
    #
    # def test_careercentersecure_staff(self):
    #     self.run_test("careercentersecure-staff", self.next_row+5)
    #
    # def test_careercentersecure_public(self):
    #     self.run_test("careercentersecure-public", self.next_row+6)
    #
    # def test_eop(self):
    #     self.run_test("eop", self.next_row+7)
    #
    # def test_eop2(self):
    #     self.run_test("eop2", self.next_row+8)
    #
    # def test_fixit(self):
    #     self.run_test("fixit", self.next_row+9)
    #
    # def test_fixit_queue(self):
    #     self.run_test("fixit-queue", self.next_row+10)
    #
    # def test_jdbs(self):
    #     self.run_test("jdbs", self.next_row+11)
    #
    # def test_orientation(self):
    #     self.run_test("orientation", self.next_row+12)

# For loop
    def test_title(self):
        with Xvfb() as xvfb:
            try:
                driver = webdriver.Firefox()
                driver.implicitly_wait(30)
                self.browser = driver
            except:
                write_log.logSetupError("firefox")
                print("Unable to load firefox")
                self.next_row += 1
                #continue

            assert(self.browser is not None)
            assert(self.sites is not None)
            browser = self.browser
            print('\n')

            # Grab each site from the dictionary.
            for siteName in self.sites:
                site = self.sites[siteName]
                # Populate spreadsheet with app name, class name, current date.
                self.spreadsheet.write_cell(self.next_row,1,siteName)
                self.spreadsheet.write_cell(self.next_row,2,type(self).__name__)
                self.spreadsheet.write_cell(self.next_row,3,self.today[:16])

                # Call the function to get status code from file check_status.py.
                result = check_status.checkStatus(site['url'], [200, 301, 302])
                if result==False:
                    print("FAIL: "+site['url']+" returns invalid http response.")
                    self.spreadsheet.write_cell(self.next_row,5,"fail\ninvalid http response")
                    self.next_row += 1
                    continue # Skip to next test in loop
                else:
                    # Begin timer
                    self.timeStart = timeit.default_timer()
                    browser.get(site['url'])
                    write_log.logInfoMsg(siteName, "title test started")
                    print("Testing " + siteName)# + " with " + browser.name.capitalize() + " Found site['title'] " + browser.title)
                    browser.implicitly_wait(30)

                    # You can also search for 'text' in browser.page_source rather than browser.title
                    if site['title'] not in browser.title:
                        self.spreadsheet.write_cell(self.next_row,5,site['title'] + " not found")
                        write_log.logErrorMsg(siteName+'\n', "Desired title '" + site['title'] + "' not found")
                        print(self.ERRORCOLOR+"ERROR:"+self.DEFAULTCOLOR+ "desired title '" + site['title'] + "' not found on " + siteName)
                        browser.save_screenshot(folderName+'/error_'+siteName+'.png')
                    else:
                        #END TIME
                        timeElapsed = timeit.default_timer() - self.timeStart
                        write_log.logSummary(self.browserType, timeElapsed)
                        # Populate spreadsheet with time and result.
                        self.spreadsheet.write_cell(self.next_row,4,round(timeElapsed, 5))
                        self.spreadsheet.write_cell(self.next_row,5,"pass")
                        write_log.logSuccess(siteName+'\n', "title")
                        print(self.SUCCESSCOLOR+"passed:"+self.DEFAULTCOLOR+ "'" + site['title'] + "' found on " + siteName)

                    self.next_row += 1



###################################
# HELPER FUNCTION #################
###################################
    # def run_test(self,siteName,row):
    #     with Xvfb() as xvfb:
    #         try:
    #             driver = webdriver.Firefox()
    #             driver.implicitly_wait(30)
    #             self.browser = driver
    #         except:
    #             write_log.logSetupError("firefox")
    #             print("Unable to load firefox")
    #
    #         assert(self.browser is not None)
    #         assert(self.sites is not None)
    #         browser = self.browser
    #         print('\n')
    #
    #         # Check that the site url exists.
    #         try:
    #             site = self.sites[siteName]
    #         except:
    #             write_log.logErrorMsg("your disk. Check to make sure the "+self.json_file+" is up to date.\n", "Test terminated prematurely. You are missing the "+siteName+" url")
    #             print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR + siteName + " credentials not found on your disk.")
    #             return
    #
    #         site = self.sites[siteName]
    #         # Populate spreadsheet with app name, class name, current date.
    #         self.spreadsheet.write_cell(row,1,siteName)
    #         self.spreadsheet.write_cell(row,2,type(self).__name__)
    #         self.spreadsheet.write_cell(row,3,self.today[:16])
    #
    #         # Once the site is found, make sure HTTP status code is 200, 301, or 302.
    #         # Call the function to get status code from file check_status.py.
    #         result = check_status.checkStatus(site['url'], [200, 301, 302])
    #         if result==False:
    #             self.spreadsheet.write_cell(row,5,"fail\ninvalid http response")
    #             return # exit test
    #         else:
    #             #BEGIN TIME
    #             self.timeStart = timeit.default_timer()
    #             browser.get(site['url'])
    #             write_log.logInfoMsg(siteName, "title test started")
    #             print("Testing " + siteName)# + " with " + browser.name.capitalize() + " Found site['title'] " + browser.title)
    #             browser.implicitly_wait(30)
    #
    #             # You can also search for 'text' in browser.page_source rather than browser.title
    #             if site['title'] not in browser.title:
    #                 self.spreadsheet.write_cell(row,5,site['title'] + " not found")
    #                 write_log.logErrorMsg(siteName+'\n', "Desired title '" + site['title'] + "' not found")
    #                 print(self.ERRORCOLOR+"ERROR:"+self.DEFAULTCOLOR+ "desired title '" + site['title'] + "' not found on " + siteName)
    #                 browser.save_screenshot(folderName+'/error_'+siteName+'.png')
    #             else:
    #                 #END TIME
    #                 timeElapsed = timeit.default_timer() - self.timeStart
    #                 write_log.logSummary(self.browserType, timeElapsed)
    #                 # Populate spreadsheet with time and result.
    #                 self.spreadsheet.write_cell(row,4,round(timeElapsed, 5))
    #                 self.spreadsheet.write_cell(row,5,"pass")
    #                 write_log.logSuccess(siteName+'\n', "title")
    #                 print(self.SUCCESSCOLOR+"passed:"+self.DEFAULTCOLOR+ "'" + site['title'] + "' found on " + siteName)
    #


# Kick off the test!
if __name__ == "__main__":
    #print("\n\u001b[33smAll test logs and screenshots will be saved to the following folder in your current directory:\n" + folderName + "\n\u001b[0m")
    unittest.main()
