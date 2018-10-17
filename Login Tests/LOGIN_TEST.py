#!/usr/local/bin/python
# coding=utf-8

# An automated browser test template written for the WebOps team at UCSC ITS.
# Requires a python3 virtualenv, LastPass CLI build, requests module imported, chrome version 59+, chromedriver version 2.38+ to run.

intro="""
----------------------------------------------------------------
File        : LOGIN_TEST.py
Description : Grab credentials from LP to log in and test sites.
Author      : Sherri Li
----------------------------------------------------------------
"""
print(intro)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import os
import unittest
import base64
import json
import datetime
import time
import timeit
import logging
import subprocess
#import sys
#sys.path.append("..")
import get_credentials
import create_log
import write_log
import status_functions


# Generate log folder and file.
folderName = create_log.createLog("ChesLpassLogin")

class LoginTest(unittest.TestCase):
    # Here are the class variables shared among all instances "self" of ChesloginTest
    ERRORCOLOR = "\u001b[31m" #red
    WARNINGCOLOR = "\u001b[33m" #yellow
    SUCCESSCOLOR = "\u001b[32m" #green
    DEFAULTCOLOR = "\u001b[0m" #white
    browser = None # webdriver instance
    browserType = None # chrome, headless chrome, or firefox
    chrome_options = None # used if testing on headless
    pwsites = None # a dictionary
    types = None # which server to test on
    timeStart = None # timer for each site
    
    while (types!='dev' and types!='dev-new' and types!='prod'):
        types = input("Enter the server you wish to test (dev, dev-new, or prod): ")
    while (browserType!='chrome' and browserType!='firefox' and browserType!='headless chrome'):
        browserType = input("Enter the browser you wish to test on (chrome, firefox, or headless chrome): ")

        
    # SETUP FUNCTIONS---------------------------------------------------------------
    # Init is a constructor that creates instances of the LoginTest object.
    def __init__(self, *args, **kwargs):
        super(LoginTest, self).__init__(*args, **kwargs)
        if self.browser is None:
            self.setupBrowser(self.browserType)
        if self.pwsites is None:
            self.setupPwSites()


    def __del__(self):
        if self.browser is not None:
            try:
                self.browser.close()
                self.browser.quit()
            except:
                pass


    # Runs before each test_method
    def setUp(self):
        if self.timeStart is None:
            self.timeStart = timeit.default_timer()

    # Runs after each test_method
    def tearDown(self):
        if self.timeStart is not None:
            timeElapsed = timeit.default_timer() - self.timeStart
            write_log.logSummary(self.browserType, timeElapsed)
            

    # Set up the webdriver instance             
    def setupBrowser(self, browserName):
        if browserName=='firefox':
            try:
                driver = webdriver.Firefox()
                driver.implicitly_wait(30)
                self.browser = driver
            except:
                print("Unable to load firefox")
        elif browserName=='headless chrome':
            try:
                self.chrome_options = Options()
                self.chrome_options.add_argument("--headless")
                driver = webdriver.Chrome(chrome_options=chrome_options)
                driver.implicitly_wait(30)
                self.browser = driver
            except:
                print("Unable to load headless chrome")
                
        else: # browserName=='chrome' default
            try:
                driver = webdriver.Chrome()
                driver.implicitly_wait(30)
                self.browser = driver
            except:
                print("Unable to load chrome")            
            
            
    # We assume that the user running the test is a member of the LastPass shared credentials folder.
    # The shared folder contains all app credentials in JSON format as a secure note.
    def setupPwSites(self):
        # Grab all credentials from the json file in lpass
        creds = get_credentials.get_all("name-of-lastpass-credential-file-here")
        # turn STRING into JSON:
        jcreds = json.loads(creds)
        self.pwsites = {}
        # MAP DICT TO DICT
        if self.types=='dev-new':
            substring = ".ucsc.edu"
            for siteData in jcreds['credentials']:
                site = {}
                # append '-new' after '-dev' in url
                url = siteData['dev_url']
                i = url.index(substring)
                site['dev_url'] = url[:i] + "-new" + url[i:]
                site['id'] = siteData['id']
                site['password'] = siteData['password']
                self.pwsites[siteData['siteName']] = site
        elif self.types=='prod':
            substring = "-dev"
            for siteData in jcreds['credentials']:
                site = {}
                # remove '-dev' from url
                site['dev_url'] = siteData['dev_url'].replace(substring, "")
                site['id'] = siteData['id']
                site['password'] = siteData['password']
                self.pwsites[siteData['siteName']] = site
        else: # self.types=='dev'
            for siteData in jcreds['credentials']:
                site = {}
                # default, no change
                site['dev_url'] = siteData['dev_url']
                site['id'] = siteData['id']
                site['password'] = siteData['password']
                self.pwsites[siteData['siteName']] = site
                

                
    # Note: Functions whose names start with "test" are automatically run by the call at the bottom 'unittest.main()'
    # TEST FUNCTIONS-------------------------------------------------------------------------
    def test_name_of_site1(self):
        self.login_with_password("text","name_of_site1","name_of_username_field","name_of_password_field")

    def test_name_of_site2(self):
        self.login_with_password("text","name_of_site2","name_of_username_field","name_of_password_field")
    
    # ... you can add more tests for the sites you want here
  

    # Note: These helper functions are not called by the unittest directly, but instead called by the test functions above.
    # HELPER FUNCTIONS-----------------------------------------------------------------------
    # Generic login to a site with a username and password box.
    def login_with_password(self, text, siteName, userboxName, passboxName):
        assert(self.browser is not None)
        assert(self.pwsites is not None)
        browser = self.browser

        # Note: define variables outside of try block so their scope is larger.
        site = None

        # Check if site credentials exist in your LastPass account.
        try:
            site = self.pwsites[siteName]
        except:
            write_log.logErrorMsg("LastPass.", "Test terminated prematurely. "+siteName+" credentials not found")
            print(self.ERRORCOLOR+"ERROR:"+self.DEFAULTCOLOR+siteName+" credentials not found in LastPass\n")
            return # Exit test

        # Make sure status code of the dev_url is 200, 301, or 302.
        result = status_functions.checkStatus(site['dev_url'], [200, 301, 302])
        if result==False:
            return # exit test

        # Open browsers to log in.
        browser.get(site['dev_url'])
        write_log.logInfoMsg(siteName, "login test started")
        print("Testing " + site['dev_url'])

        usernameBox = None
        passwordBox = None

        try:
            usernameBox = browser.find_element_by_name(userboxName)
        except:
            write_log.logButtonMissing(site['url'], "Login field")
            print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+"could not locate login field\n")
            return
        try:
            passwordBox = browser.find_element_by_name(passboxName)
        except:
            write_log.logButtonMissing(site['url'], "Password field")
            print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+"could not locate password field\n")
            return

        usernameBox.clear()
        usernameBox.send_keys(site['id'])
        passwordBox.clear()
        passwordBox.send_keys(site['password'])
        passwordBox.send_keys(Keys.ENTER)

        browser.implicitly_wait(30)

        if text not in browser.page_source:
            write_log.logErrorMsg(siteName+'\n', "Login test failed")
            print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+"'"+text+"' not found on "+siteName+" after successful login\n")
            return
        # can also assert(text in browser.page_source)

        #TODO: Add a logout feature
        write_log.logSuccess(siteName+'\n', "login")
        print(self.SUCCESSCOLOR+"passed: "+self.DEFAULTCOLOR+"login to "+siteName+'\n')



# Begin the test            
if __name__ == "__main__":
    username = ""
    while "@" not in username:
        username = input("Enter LastPass username (your email): ")
    # use LastPass CLI commands to kick off the login process
    subprocess.call(['lpass', 'login', username])
    # run all functions in the login_test class
    unittest.main()
