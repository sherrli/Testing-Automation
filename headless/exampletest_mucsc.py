#!/usr/local/bin/python
# coding=utf-8

# Headless firefox title test for jenkins build.

intro="""
----------------------------------------------------------------
File        : exampletest_mucsc.py
Description : Test for m.ucsc.edu, example of a solo smoke test.
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



# Generate log folder and file.
# Default log level is INFO (everything). Go to create_log.py to change.
#folderName = create_log.createLog("ChesProdTitle")

class MUcscTest(unittest.TestCase):
    browser = None
    site = 'https://m.ucsc.edu/'


###################################
# SETUP FUNCTIONS #################
###################################
    def __init__(self, *args, **kwargs):
        super(MUcscTest, self).__init__(*args, **kwargs)
        # subclass

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

            try:
                # Check that HTTP status code is 200, 301, or 302.
                # Call the function to get status code from file check_status.py.
                result = check_status.checkStatus(site, [200, 301, 302])
                if result != True:
                    print("FAIL: "+site['url']+" returns invalid http response code of "+str(result))

                assert(result==True)

                # Open browser in headless.
                browser.get(site)
                timeStart = timeit.default_timer()
                print("Opening " + site)
                browser.implicitly_wait(30)

                # Locate some elements here
                browser.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Map'])[2]/i[1]").click()

                # Assert some button/web element is present
                assert(browser.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Shuttle Routes'])[1]/following::label[1]") is not None)

                timeElapsed = timeit.default_timer() - timeStart
                print("passed: " + site + " tested in " + str(round(timeElapsed, 4)) + " seconds")

            except Exception as e:
                print(e)
                raise e


# Kick off the test!
if __name__ == "__main__":
    #print("\n\u001b[33smAll test logs and screenshots will be saved to the following folder in your current directory:\n" + folderName + "\n\u001b[0m")
    unittest.main()
