#!/usr/local/bin/python
# coding=utf-8

from selenium import webdriver
import unittest
import os
import json
import time
import datetime
import timeit
import logging
import sys
sys.path.append("..")
import write_log
import check_status
import create_log


# Generate log folder and file.
# Default log level is INFO (everything). Go to create_log.py to change.
folderName = create_log.createLog("ChesProdTitle")

class ChesProdTest(unittest.TestCase):
    # Name of the JSON file containing the sites to test
    json_file = "sites-prod.json" # can modify later

    # Here are the class variables shared among all instances "self" of ChesDevNewTitleTest
    ERRORCOLOR = "\u001b[31m" #red
    WARNINGCOLOR = "\u001b[33m" #yellow
    SUCCESSCOLOR = "\u001b[32m" #green
    DEFAULTCOLOR = "\u001b[0m" #white
    browser = None
    browserType = None
    sites = None

    timeStart = None

    while (browserType!='chrome' and browserType!='firefox'):
        browserType = input("Enter the browser you wish to test on (chrome or firefox): ")


# SETUP FUNCTIONS------------------------------------------------------------------

    def __init__(self, *args, **kwargs):
        super(ChesProdTest, self).__init__(*args, **kwargs)
        if self.browser is None:
            self.setupBrowser()
        if self.sites is None:
            self.setupSites()

    def __del__(self):
        if self.browser is not None:
            try:
                self.browser.close()
                self.browser.quit()
            except:
                pass

    def setUp(self):
        if self.timeStart is None:
            self.timeStart = timeit.default_timer()

    def tearDown(self):
        if self.timeStart is not None:
            timeElapsed = timeit.default_timer() - self.timeStart
            write_log.logSummary(self.browserType, timeElapsed)

    def setupBrowser(self):
        if self.browserType=='firefox':
            try:
                driver = webdriver.Firefox()
                driver.implicitly_wait(30)
                self.browser = driver
            except:
                write_log.logSetupError("firefox")
                print("Unable to load firefox")
        else: # default to chrome
            try:
                driver = webdriver.Chrome()
                driver.implicitly_wait(30)
                self.browser = driver
            except:
                write_log.logSetupError("chrome")
                print("Unable to load chrome")

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


# TEST FUNCTIONS--------------------------------------------------------------

    def test_admissions(self):
        self.run_test('admissions')

    def test_admstats(self):
        self.run_test("admstats")

    def test_btconference(self):
        self.run_test("btconference")

#     def test_common(self):
#         self.run_test("common")

    def test_conrooms(self):
        self.run_test("conrooms")

    def test_careercentersecure_student(self):
        self.run_test("careercentersecure-student")

    def test_careercentersecure_staff(self):
        self.run_test("careercentersecure-staff")

    def test_careercentersecure_public(self):
        self.run_test("careercentersecure-public")

#     def test_eds(self):
#         self.run_test("eds")

    def test_eop(self):
        self.run_test("eop")

    def test_eop2(self):
        self.run_test("eop2")
#
    def test_fixit(self):
        self.run_test("fixit")

    def test_fixit_queue(self):
        self.run_test("fixit-queue")
#
    def test_jdbs(self):
        self.run_test("jdbs")
#
    def test_orientation(self):
        self.run_test("orientation")

#     def test_ucforyoutransfer(self):
#         self.run_test("ucforyoutransfer")

#     def test_volunteer(self):
#         self.run_test("volunteer")


# HELPER FUNCTION-------------------------------------------------------------------

    def run_test(self,siteName):
        assert(self.browser is not None)
        assert(self.sites is not None)
        browser = self.browser
        print('\n')

        # Check that the site url exists.
        try:
            site = self.sites[siteName]
        except:
            write_log.logErrorMsg("your disk. Check to make sure the "+self.json_file+" is up to date.\n", "Test terminated prematurely. You are missing the "+siteName+" url")
            print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR + siteName + " credentials not found on your disk.")
            return

        site = self.sites[siteName]

        # Once the site is found, make sure HTTP status code is 200, 301, or 302.
        # Call the function to get status code from file check_status.py.
        result = check_status.checkStatus(site['url'], [200, 301, 302])
        if result==False:
            return # exit test

        try:
            browser.get(site['url'])
            write_log.logInfoMsg(siteName, "title test started")
            print("Testing " + siteName)# + " with " + browser.name.capitalize() + " Found site['title'] " + browser.title)
            browser.implicitly_wait(30)

            # You can also search for 'text' in browser.page_source rather than browser.title
            if site['title'] not in browser.title:
                write_log.logErrorMsg(siteName+'\n', "Desired title '" + site['title'] + "' not found")
                print(self.ERRORCOLOR+"ERROR:"+self.DEFAULTCOLOR+ "desired title '" + site['title'] + "' not found on " + siteName)
                browser.save_screenshot(folderName+'/error_'+siteName+'.png')
            else:
                write_log.logSuccess(siteName+'\n', "title")
                print(self.SUCCESSCOLOR+"passed:"+self.DEFAULTCOLOR+ "'" + site['title'] + "' found on " + siteName)

            #print("PASS: %s using %s" % (siteName,browser.name.capitalize()))

        except Exception as e:
            print(e)
            #raise e
        finally:
            browser.close()


# Kick off the test!
if __name__ == "__main__":
    #print("\n\u001b[33smAll test logs and screenshots will be saved to the following folder in your current directory:\n" + folderName + "\n\u001b[0m")
    unittest.main()
