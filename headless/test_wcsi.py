#!/usr/local/bin/python
# coding=utf-8

# Headless selenium test used in the Jenkins pipeline.

intro="""
----------------------------------------------------------------
File        : exampletest_wcsi.py
Description : Solo test for wcsi, write to spreadsheet.
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
import check_status
import spreadsheet


class WcsiTest(unittest.TestCase):
    browser = None
    site = 'https://webapps.ucsc.edu/wcsi'
    siteName = 'Wcsi'
    today = str(datetime.datetime.now())


###################################
# SETUP FUNCTIONS #################
###################################
    def __init__(self, *args, **kwargs):
        super(WcsiTest, self).__init__(*args, **kwargs)
        self.spreadsheet = spreadsheet.Spreadsheet()
        self.spreadsheet.open_sheet(str(type(self).__name__))
        self.next_row = self.spreadsheet.next_available_row() + 1

    def __del__(self):
        if self.browser is not None:
            try:
                self.browser.quit()
            except Exception as e:
                pass
###################################
# TEST FUNCTION ###################
###################################
# Functions beginning with the string 'test' run automatically when script is called.
# Parameter is self, which includes the 2 variables defined under the class definition: browser, site.
    def test_mucsc(self):
        with Xvfb() as xvfb:
            try:
                driver = webdriver.Firefox()
                driver.implicitly_wait(30)
                self.browser = driver
            except:
                print("Unable to load firefox")

            assert(self.browser is not None)
            browser = self.browser
            site = self.site
            row = self.next_row

            try:
                self.spreadsheet.write_cell(row,1,siteName)
                self.spreadsheet.write_cell(row,2,type(self).__name__)
                self.spreadsheet.write_cell(row,3, site)
                self.spreadsheet.write_cell(row,4,self.today[:16])
                # Check that HTTP status code is 200, 301, or 302.
                # Call the function to get status code from file check_status.py.
                result = check_status.checkStatus(site, [200, 301, 302])
                if result != True:
                    self.spreadsheet.write_cell(row,5,"fail\nstatus " + result)
                    print("FAIL: "+site+" returns invalid http response code of "+str(result))
                assert(result==True)

                # Open browser in headless.
                browser.get(site)
                timeStart = timeit.default_timer()
                print("Opening " + site)
                browser.implicitly_wait(30)

                # Locate some elements here
                browser.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Cancel'])[1]/following::input[1]").click()

                # Assert some button/web element is present
                #assert(browser.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='Sexual Violence Prevention & Response'])[1]/following::span[3]") is not None)
                # Click the Course His-09 in Spring 2019
                browser.find_element_by_link_text("Intr Native Am His").click()
                # Assert that link to catalog is present
                assert(browser.find_element_by_link_text("History Course Catalog") is not None)
                self.spreadsheet.write_cell(row,5,"pass")
                timeElapsed = timeit.default_timer() - timeStart
                self.spreadsheet.write_cell(row,6,round(timeElapsed, 5))
                print("passed: " + site + " tested in " + str(round(timeElapsed, 4)) + " seconds")

            except Exception as e:
                self.spreadsheet.write_cell(row,5,"fail")
                print(e)
                raise e


# Kick off the test!
if __name__ == "__main__":
    #print("\n\u001b[33smAll test logs and screenshots will be saved to the following folder in your current directory:\n" + folderName + "\n\u001b[0m")
    unittest.main()
