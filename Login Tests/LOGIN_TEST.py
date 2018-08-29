#!/usr/local/bin/python
# coding=utf-8
# An automated browser login test template written for the WebOps team at UCSC ITS.
# Some web apps have a ID and PASSWORD to log in, others require ID and three BIRTHDAY mm-dd-year fields.

intro="""
----------------------------------------------------------------
File        : LOGIN_TEST.py
Description : Grab credentials from LP to log in and test sites.
Author      : Sherri Li
----------------------------------------------------------------
"""
print(intro)

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import base64
import os
import json
import datetime
import time
import subprocess
#import sys
#sys.path.append("..")
import lastpass-login
import log-test
import site-functions

# This test generates a log file whose file name is dynamically generated, based on system time.
# Get the date formatted as year-mm-dd_hr:min.
timeOfTest = str(datetime.datetime.now()).replace(' ', '')[0:16]
logging.basicConfig(filename=timeOfTest + '_LoginTest.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

class login_test(unittest.TestCase):
    appName = 'ches-dev' # can change to whatever group of apps you wish to test
    browser = None
    browserType = None
    pwsites = None
    bdsites = None
    types = None
    while (types!='dev' and types!='dev-new' and types!='prod'):
        types = input("Enter the server you wish to test (dev, dev-new, or prod): ")
    while (browserType!='chrome' and browserType!='firefox'):
        browserType = input("Enter the browser you wish to test on (chrome or firefox): ")

    # init is a constructor that runs for every test module below
    def __init__(self, *args, **kwargs):
        super(login_test, self).__init__(*args, **kwargs)
        if self.browser is None:
            self.setupBrowser(self.browserType)
        if self.pwsites is None:
            self.setupPwSites()
        if self.bdsites is None:
            self.setupBdSites()


    def __del__(self):
        if self.browser is not None:
            try:
                self.browser.close()
                self.browser.quit()
            except:
                pass


    def setUp(self):
        username = None
        password = None
        mm = None
        dd = None
        yr = None

    def tearDown(self):
        pass


#CASE ONE: all credentials are in one LastPass file
    def setupPwSites(self):
        # Grab all credentials from the json file in lpass
        creds = login_lp.get_all(self.appName+'-pw-creds.json')
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


    def setupBdSites(self):
        # CALL LOGIN_LP HERE INSTEAD
        # SAVE THE RETURN STRING TO A PYTHON LIST/DICT
        creds = login_lp.get_all(self.appName+'-bd-creds.json')
        jcreds = json.loads(creds)
        self.bdsites = {}
        if self.types=='dev-new':
            substring = ".ucsc.edu"
            for siteData in jcreds['credentials']:
                site = {}
                # append '-new' after '-dev'
                url = siteData['dev_url']
                i = url.index(substring)
                site['dev_url'] = url[:i] + "-new" + url[i:]
                site['id'] = siteData['id']
                site['mm'] = siteData['mm']
                site['dd'] = siteData['dd']
                site['yr'] = siteData['yr']
                self.bdsites[siteData['siteName']] = site
        elif self.types=='prod':
            substring = "-dev"
            for siteData in jcreds['credentials']:
                site = {}
                # remove '-dev' from default url
                site['dev_url'] = siteData['dev_url'].replace(substring, "")
                site['id'] = siteData['id']
                site['mm'] = siteData['mm']
                site['dd'] = siteData['dd']
                site['yr'] = siteData['yr']
                self.bdsites[siteData['siteName']] = site
        else: # self.types=='dev'
            for siteData in jcreds['credentials']:
                site = {}
                # default, no change
                site['dev_url'] = siteData['dev_url']
                site['id'] = siteData['id']
                site['mm'] = siteData['mm']
                site['dd'] = siteData['dd']
                site['yr'] = siteData['yr']
                self.bdsites[siteData['siteName']] = site


# TODO: CASE TWO: each site has its own credentials file in LastPass


    def setupBrowser(self, browserName):
        if browserName=='firefox':
            try:
                driver = webdriver.Firefox()
                driver.implicitly_wait(30)
                self.browser = driver
            except:
                print("Unable to load firefox")
        else: # browserName=='chrome' default
            try:
                driver = webdriver.Chrome()
                driver.implicitly_wait(30)
                self.browser = driver
            except:
                print("Unable to load chrome")

    # Note: only functions whose names start with "test" get automatically run by the call at the bottom 'unittest.main()'

    def test_name_of_site1(self):
        self.password_login_test("name_of_site","name_of_username_field","name_of_password_field","name_of_submit_button")

    def test_name_of_site2(self):
        self.birthday_login_test("name_of_site","name_of_username_field","name_of_month_field","name_of_day_field","name_of_year_field","name_of_submit_button")
    
    # ... you can add more tests for the sites you want here
    

    # Generic login test to a site requiring USERNAME and PASSWORD credentials
    def password_login_test(self,siteName,usernameBox,passwordBox,loginButtonName):
        assert(self.browser is not None)
        assert(self.pwsites is not None)
        text = "Work-study Information"
        browser = self.browser
        
        # Make sure the site credentials exist in your LastPass
        try:
            site = self.pwsites[siteName]
        except:
            print("ERROR: " + siteName + " credentials not found in your LastPass account")
            return

        site = self.pwsites[siteName]

        # First ensure HTTP status code is 200, 301, or 302.
        # Call a function from the site-functions.py file to get the http status code.
        result = site-functions.get_status(site['dev_url'])
        if result==False:
            return # exit test

        # Open drivers after ensuring status code is acceptable.
        try:
            browser.get(site['dev_url'])
            # Call function from log-test.py file to write message to log file
            log-test.logStart("name_of_site_you_are_testing_here")
            print("Testing " + site['dev_url'])

            self.username = site['id']
            self.password = site['password']
            username_txt = browser.find_element_by_name(usernameBox)
            password_txt = browser.find_element_by_name(passwordBox)
            #submit_txt = browser.find_element_by_xpath("(//input[@name='act'])[2]")
            #submit_txt.send_keys(Keys.TAB) # tab over to not-visibile element
            assert(username_txt is not None)
            assert(password_txt is not None)
            #assert(submit_txt is not None)

            username_txt.clear()
            username_txt.send_keys(self.username)
            password_txt.clear()
            password_txt.send_keys(self.password)
            #submit_txt.click()
            browser.find_element_by_name(passwordBox).send_keys(Keys.ENTER) # submit button sometimes not visible

            if text not in browser.page_source:
                print("ERROR: " + text + " not in " + siteName + " source after successful login\n")
            assert(text in browser.page_source)

            logout_txt = browser.find_element_by_xpath("//area") # parametrize to logoutButtonName
            if logout_txt==None:
                print(siteName + " has no logout button")
            assert(logout_txt is not None)
            logout_txt.click()
            
            log-test.logSuccess("name_of_site_you_are_testing_here", "login")
            print("passed %s\n" % (siteName))#(siteName,browser.name.capitalize()))

        except Exception as e:
            print(e)
            raise e
        finally:
            browser.close()

    # Generic login test to a site requiring USERNAME and BIRTHDAY credentials
    def birthday_login_test(self,siteName,usernameBox,monthBox,dayBox,yearBox,loginButtonName):
        assert(self.browser is not None)
        assert(self.bdsites is not None)
        text = "Account Options"
        browser = self.browser
        
        # Make sure the site credentials exist in your LastPass
        try:
            site = self.bdsites[siteName]
        except:
            print("ERROR: " + siteName + " credentials not found in your LastPass account")
            return

        site = self.bdsites[siteName]

        # First ensure HTTP status code is 200, 301, or 302.
        # Call a function from the site-functions.py file to get the http status code.
        result = site-functions.get_status(site['dev_url'])
        if result==False:
            return # exit test
        
        # Open drivers after ensuring status code was acceptable.
        try:
            browser.get(site['dev_url'])
            # Call function from log-test.py file to write message to log file
            log-test.logStart("name_of_site_you_are_testing_here")
            print("Testing " + site['dev_url'])

            self.username = site['id']
            self.mm = site['mm']
            self.dd = site['dd']
            self.yr = site['yr']

            username_txt = browser.find_element_by_name(usernameBox)
            password_mm = browser.find_element_by_id(monthBox)
            password_dd = browser.find_element_by_id(dayBox)
            password_yr = browser.find_element_by_id(yearBox)
            submit_txt = browser.find_element_by_name(loginButtonName)
            assert(username_txt is not None)
            assert(password_mm is not None)
            assert(password_dd is not None)
            assert(password_yr is not None)
            assert(submit_txt is not None)

            username_txt.clear()
            password_mm.clear()
            password_dd.clear()
            password_yr.clear()
            username_txt.send_keys(self.username)
            password_mm.send_keys(self.mm)
            password_dd.send_keys(self.dd)
            password_yr.send_keys(self.yr)
            submit_txt.click()

            if text not in browser.page_source:
                print("ERROR: " + text + " not in " + siteName + " source after successful login\n")
            assert(text in browser.page_source)

            #logout_txt = browser.find_element_by_name('logout') # TODO parametrize logout button name
            #assert(logout_txt is not None)
            #logout_txt.click()
            
            log-test.logSuccess("name_of_site_you_are_testing_here", "login")
            print("passed %s\n" % (siteName))#(siteName,browser.name.capitalize()))

        except Exception as e:
            print(e)
            raise e
        finally:
            browser.close()


            
if __name__ == "__main__":
    username = ""
    while "@ucsc.edu" not in username:
        username = input("Enter LastPass username (Make sure to include @ucsc.edu): ")
    # use LastPass CLI commands to kick off the login process
    subprocess.call(['lpass', 'login', username])
    # run all functions in the login_test class
    unittest.main()
