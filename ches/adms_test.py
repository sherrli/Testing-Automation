#!/usr/local/bin/python
# coding=utf-8


# Verify that legacy data correctly populates in admstats.
# Gives user the option to choose chrome or firefox, and dev/dev-new/prod.
# Pre-condition: your UCSC LastPass account is part of the shared folder: Selenium-ColdFusion.


intro="""
----------------------------------------------------------------
Name        : ADMS test
Description : Click links, verify data is present on ADMS servers.
Author      : Sherri
File        : adms_test.py
----------------------------------------------------------------
"""
print(intro)


import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import timeit
import datetime
import requests
import logging
import os
import sys
sys.path.append("..")
import write_log
import create_log
import check_status

# Generate log folder and file.
folderName = create_log.createLog("Adms")

class adms_test(unittest.TestCase):
    ERRORCOLOR = "\u001b[31m" #red
    WARNINGCOLOR = "\u001b[33m" #yellow
    SUCCESSCOLOR = "\u001b[32m" #green
    DEFAULTCOLOR = "\u001b[0m" #white
    browser = None
    browserType = None
    site = None
    siteType = None
    timeStart = None
    while (browserType!="chrome" and browserType!="firefox"):
        browserType = input("Enter the browser you wish to test on (chrome or firefox): ")
    while (siteType!="prod" and siteType!="dev" and siteType!="dev-new"):
        siteType = input("Enter the server you wish to test (dev, dev-new, or prod): ")


    def __init__(self, *args, **kwargs):
        super(adms_test, self).__init__(*args, **kwargs)
        if self.browser is None:
            self.setupBrowser()
        if self.site is None:
            self.setupSite()

    def __del__(self):
        if self.browser is not None:
            try:
                self.browser.close()
                self.browser.quit()
            except:
                pass

    def setUp(self):
        self.timeStart = timeit.default_timer()
        print("timer started")

    def tearDown(self):
        if self.timeStart is not None:
            timeElapsed = timeit.default_timer() - self.timeStart
            write_log.logSummary(self.browserType, timeElapsed)
            print("timer stopped")
        else:
            print("timer failed")

    def setupBrowser(self):
        if self.browserType=='firefox':
            try:
                driver = webdriver.Firefox()
                driver.implicitly_wait(30)
                self.browser = driver
            except:
                write_log.logSetupError("firefox")
                print("Unable to load firefox")
        else: # default to CHROME
            try:
                driver = webdriver.Chrome()
                #If webdriver.Chrome() does not work on your Mac, use below:
                #chrome = webdriver.Chrome('/usr/local/bin/chromedriver')
                driver.implicitly_wait(30)
                self.browser = driver
            except:
                write_log.logSetupErro("chrome")
                print("Unable to load chrome")

    def setupSite(self):
        if self.siteType=='prod':
            self.site = "https://admstats.sa.ucsc.edu/"
        elif self.siteType=='dev-new':
            self.site = "https://admstats.sa-dev-new.ucsc.edu/"
        else: # default to dev
            self.site = "https://admstats.sa-dev.ucsc.edu/"


# HELPER FUNCTION-------------------
    def findText(self, text, test):
        if text not in self.browser.page_source:
            write_log.logErrorMsg(self.browser.current_url, text + " not found")
            print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+text+" not found on "+test)
            browser.save_screenshot(folderName+'/error_'+test+'_admstest.png')


# TEST FUNCTION=------------------functions beginning with "test" automatically run
    # Check that "Overall" data is present in Fall, Winter, Spring.
    def test_fws(self):
        assert(self.browser is not None)
        assert(self.site is not None)
        # Make abbreviations for browser and site name variables
        browser = self.browser
        site = self.site

        # Once the site is found, make sure HTTP status code is 200, 301, or 302.
        # Call the function to get status code from file check_status.py.
        result = check_status.checkStatus(site['url'], [200, 301, 302])
        if result==False:
            return # exit test


        # Begin the actual test after status code is confirmed.
        try:
            browser.get(site)
            write_log.logStart(site)
            print("Testing " + site)
            #frame = browser.find_element_by_xpath('//frame[@name="main"]')
            #browser.switch_to.frame(frame)

            # Timeout after 30 seconds
            WebDriverWait(browser, 30).until(EC.title_contains("Admissions Statistics"))
            if "UCSC Undergraduate Admissions Statistics" not in browser.title:
                write_log.logErrorMsg(browser.current_url, "'UCSC Undergraduate Admissions Statistics' not found")
                print(self.ERRORCOLOR+"ERROR:"+self.DEFAULTCOLOR+" title test failed on homepage")
                browser.save_screenshot(folderName+'/error_home_admstest.png')
            if "or by selecting from the table below:" not in browser.page_source:
                write_log.logErrorMsg(browser.current_url, "'from the table below' text not found")
                print(self.ERRORCOLOR+"ERROR:"+self.DEFAULTCOLOR+" text missing on homepage")

#TODO: output the exact text that should have been found on the sites but was not Found
#TODO: this is a fix for all the print("ERROR") lines...

            # Go to Fall------------------------------------------------------
            # link = browser.find_element_by_link_text('Fall Quarters') # no such element found!?
            link = browser.find_element_by_xpath("//a/font")
            link.click()
            WebDriverWait(browser, 10).until(EC.title_contains("Fall Quarter"))
            if "UCSC Undergraduate Admissions Statistics --- Fall Quarter" not in browser.title:
                write_log.logErrorMsg(browser.current_url, "Fall Quarter title not found")
                print(self.ERRORCOLOR+"ERROR:"+self.DEFAULTCOLOR+" title test failed on Fall Quarters page")
                browser.save_screenshot(folderName+'/error_fall_admstest.png')

            # Title and Data tests for Overall Fall 2003----------------------
            browser.find_element_by_link_text("Overall").click()
            WebDriverWait(browser, 10).until(EC.title_contains("Applications"))
            if "Admissions Stats: Summary of Applications" not in browser.title:
                write_log.logErrorMsg(browser.current_url, "Summary of Applications text not found")
                print(self.ERRORCOLOR+"ERROR:"+self.DEFAULTCOLOR+" title test failed on Fall 2003 overall data page")
                browser.save_screenshot(folderName+'/error_fall03_admstest.png')

# TODO: make generic check source code function for 3 lines
            if "21,801" not in browser.page_source and "Summary of Applications: Fall 2003" in browser.page_source:
                write_log.logErrorMsg(browser.current_url, "data not found in Fall 2003")
                print(self.ERRORCOLOR+"ERROR:"+self.DEFAULTCOLOR+" data failed to populate in Fall 2003 Application Summary")
                browser.save_screenshot(folderName+'/error_fall03data_admstest.png')
            elif "21,801" not in browser.page_source:
                print(self.ERRORCOLOR+"ERROR:"+self.DEFAULTCOLOR+" Test not up to date. See source code.\nREPLACE 21,801 with a different value.")
            else:
                write_log.logSuccess(site+'\n', "fall data population")
                print(self.SUCCESSCOLOR+"passed:"+self.DEFAULTCOLOR+" fall data test")
                browser.save_screenshot(folderName+'/success_fall03_admstest.png')

            browser.back()
            browser.back()
            if "Winter Quarters" not in browser.page_source:
                write_log.logErrorMsg(browser.current_url, "Back button not working")
                print(self.ERRORCOLOR+"ERROR:"+self.DEFAULTCOLOR+" back() not working, must modify test")
            assert("Winter Quarters" in browser.page_source)

            # Go to Winter----------------------------------------------------
            link = browser.find_element_by_xpath("//li[2]/a/font")
            link.click()
            WebDriverWait(browser, 10).until(EC.title_contains("Winter Quarter"))
            if "UCSC Undergraduate Admissions Statistics --- Winter Quarter" not in browser.title:
                write_log.logErrorMsg(browser.current_url, "Winter Quarter title not found")
                print(self.ERRORCOLOR+"ERROR:"+self.DEFAULTCOLOR+" title test failed on Winter Quarters page")
                browser.save_screenshot(folderName+'/error_winter_admstest.png')

            # Title and Data tests for Overall Winter 2003--------------------
            browser.find_element_by_xpath("(//a[contains(text(),'Overall')])[2]").click()
            WebDriverWait(browser, 10).until(EC.title_contains("Applications"))
            if "Admissions Stats: Summary of Applications" not in browser.title:
                write_log.logErrorMsg(browser.current_url, "Summary of Applications title not found")
                print(self.ERRORCOLOR+"ERROR:"+self.DEFAULTCOLOR+" title test failed on Winter 2003 overall data page")
                browser.save_screenshot(folderName+'/error_winterapp_admstest.png')

            if "-0.6" not in browser.page_source and "Summary of Applications: Winter 2003" in browser.page_source:
                write_log.logErrorMsg(browser.current_url, "data not found in Winter 2003")
                print(self.ERRORCOLOR+"ERROR:"+self.DEFAULTCOLOR+" data failed to populate in Winter 2003 Application Summary")
                browser.save_screenshot(folderName+'/error_winter03_admstest.png')
            elif "-0.6" not in browser.page_source:
                print(self.ERRORCOLOR+"ERROR:"+self.DEFAULTCOLOR+" Test not up to date. See source code.\nREPLACE '-0.6' in line 123-126 with a different value.")
            else:
                write_log.logSuccess(site+'\n', "winter data population")
                print(self.SUCCESSCOLOR+"passed:"+self.DEFAULTCOLOR+" winter data test")
                browser.save_screenshot(folderName+'/success_winter03_admstest.png')

            browser.back()
            browser.back()
            if "Spring Quarters" not in browser.page_source:
                write_log.logErrorMsg(browser.current_url, "Back button not working")
                print(self.ERRORCOLOR+"ERROR:"+self.DEFAULTCOLOR+" back() not working, must modify test")
            assert("Spring Quarters" in browser.page_source)

            # Go to Spring----------------------------------------------------
            link = browser.find_element_by_xpath("//li[3]/a/font") # font was <LI>
            link.click()
            WebDriverWait(browser, 10).until(EC.title_contains("Spring Quarter"))
            if "UCSC Undergraduate Admissions Statistics --- Spring Quarter" not in browser.title:
                write_log.logErrorMsg(browser.current_url, "Spring Quarter title not found")
                print(self.ERRORCOLOR+"ERROR:"+self.DEFAULTCOLOR+" title test failed on Spring Quarters page")
                browser.save_screenshot(folderName+'/error_spring_admstest.png')

            # Title and Data tests for Overall Spring 1992--------------------
            browser.find_element_by_link_text("Overall").click()
            WebDriverWait(browser, 10).until(EC.title_contains("Applications"))
            if "Spring 1992 Summary of Applications" not in browser.title:
                write_log.logErrorMsg(browser.current_url, "Spring 1992 Summary of Applications title not loading")
                print(self.ERRORCOLOR+"ERROR:"+self.DEFAULTCOLOR+" title test failed on Spring 1992 overall data page")
                browser.save_screenshot(folderName+'/error_springapp_admstest.png')

            if "542.9" not in browser.page_source and browser.title=="Spring 1992 Summary of Applications":
                write_log.logErrorMsg(browser.current_url, "data not found in Spring 1992")
                print(self.ERRORCOLOR+"ERROR:"+self.DEFAULTCOLOR+" data failed to populate in Spring 1992 Application Summary")
                browser.save_screenshot(folderName+'/error_spring92_admstest.png')
            elif "542.9" not in browser.page_source:
                print(self.ERRORCOLOR+"ERROR:"+self.DEFAULTCOLOR+" Test not up to date. See source code.\nREPLACE '542.9' in line 147-150 with a different value.")
            else:
                write_log.logSuccess(site+'\n', "spring data population")
                print(self.SUCCESSCOLOR+"passed:"+self.DEFAULTCOLOR+" spring data test")
                browser.save_screenshot(folderName+'/success_spring92_admstest.png')

        except Exception as e:
            print(e)
            raise(e)


if __name__ == "__main__":
    #print("\n\u001b[33mAll test logs and screenshots will be saved to the following folder in your current directory:\n" + folderName + "\n\u001b[0m")
    time.sleep(3)
    unittest.main()
