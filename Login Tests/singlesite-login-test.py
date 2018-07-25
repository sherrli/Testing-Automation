#!/usr/local/bin/python
# coding=utf-8


intro="""
----------------------------------------------------------------
File        : unit_login_test.py
Description : Generic template to log in by grabbing individual
              site credentials from LastPass.
              LastPass Site Naming Convention:
                    "name-typeofuser-cred"
Author      : shli17
----------------------------------------------------------------
"""
print(intro)

import lastpass-login
import subprocess
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class GenericLoginTest(unittest.TestCase):
    browsers = None
    types = None
    sites = None # sites is a dictionary of dictionaries.
    siteList = []
    while (types!='dev' and types!='dev-new' and types!='prod'):
        types = input("Enter the server you wish to test (dev, dev-new, or prod): ")
        if types=='prod':
            answer = input("Warning - these tests write to the database. Type prod to confirm: ")
            if answer!='yes':
                types = None # reset to beginning of loop
    print("Enter the sites you wish to test, separated by spaces.")

    siteNames = input("For example: careercenter-staff careercenter-supervisor careercenter-student eop-admin eop-msi eop-student\nPress enter after you are done: ")
    siteList = siteNames.split()

    # __init__ runs once before all other methods
    def __init__(self, *args, **kwargs):
        super(GenericLoginTest, self).__init__(*args, **kwargs)
        if self.browsers is None:
            self.setupBrowsers()
        if self.sites is None:
            self.sites = {}
            for site in siteList:
                self.setupSite(site)

    def __del__(self):
        if self.browsers is not None:
            for browser in self.browsers:
                try:
                    browser.close()
                    browser.quit()
                except:
                    pass

    # setUp is run once before each test instance
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def setupBrowsers(self):
        self.browsers=[]
        try:
            chrome = webdriver.Chrome()
            chrome.implicitly_wait(30)
            self.browsers.append(chrome)
        except:
            print("Unable to load chrome")


    def setupSite(self, siteName):
        cred = lastpass-login.get_item(siteName + '-cred')
        if self.types=='dev-new':
            substring = ".ucsc.edu"
            site = {}
            # append '-new' after '-dev' in url
            i = (cred.url).index(substring)
            site['url'] = (cred.url)[:i] + "-new" + (cred.url)[i:]
            site['username'] = cred.user
            site['password'] = cred.pw
            self.sites[siteName] = site
        elif self.types=='prod':
            site = {}
            site['url'] = (cred.url).replace("-dev", "")
            site['username'] = cred.user
            site['password'] = cred.pw
            self.sites[siteName] = site
        else: # default to self.types=='dev'
            site = {}
            site['url'] = cred.url
            site['username'] = cred.user
            site['password'] = cred.pw
            self.sites[siteName] = site


    # test_run calls login_test on each site in the class variable sites
    def test_run(self):
        for siteName in self.sites:
            self.login_test(siteName)

    def login_test(self, siteName):
        assert(self.browsers is not None)
        assert(self.sites is not None)
        for browser in self.browsers:
            try:
                site = self.sites[siteName]
                if not site:
                    print("Could not find %s")
                browser.get(site['url'])
                print("Testing " + site['url'])

                # Grabbing the first text input box works 80% of the time for 20% of the effort
                usernameBox = driver.find_element_by_xpath('//input[@type="text"]')
                passwordBox = driver.find_element_by_xpath('//input[@type="password"]')

                if not usernameBox:
                    print("ERROR: could not locate the login box")
                if not passwordBox:
                    # TODO: Determine if the site requires 3 birthday fields or 1 password field
                    if "/" in site['password'] and browser.contains_3_password_input_elements:
                        birthday_list = site['password'].split("/")
                        mm = birthday_list[0]
                        dd = birthday_list[1]
                        yr = birthday_list[2]
                # print("ERROR: could not locate the password box")
                assert(usernameBox is not None)
                assert(passwordBox is not None)
                usernameBox.clear()
                passwordBox.clear()

                usernameBox.send_keys(site['username'])
                passwordBox.send_keys(site['password'])
                passwordBox.send_keys(Keys.ENTER)
                browser.implicitly_wait(10)

                # Verify login success
                #TODO: check for title text
                print("passed: login to " + siteName)

                # Verify logout success
                #TODO: find and click logout button
                print("passed: logout of " + siteName)

            except Exception as e:
                print(e)
                raise(e)
            finally:
                browser.close()


if __name__ == "__main__":
    username = ""
    while "@ucsc.edu" not in username:
        username = input("Enter LastPass username: ")

    subprocess.call(['lpass', 'login', username])
    unittest.main()
