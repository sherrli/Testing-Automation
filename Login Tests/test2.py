#!/usr/local/bin/python
# coding=utf-8


# Advanced tests that modify the dev/stage databases of cruzidmanager and grouper.
# Pre-condition: your UCSC LastPass account is part of the shared folder: Selenium-ColdFusion.


intro="""
----------------------------------------------------------------
File        : idm_test.py
Description : Log in using LastPass CLI and create groups/users.
Author      : Sherri Li
----------------------------------------------------------------
"""
print(intro)

import sys
sys.path.append("..")
import return_credentials # functions to grab lastpass credentials
import write_log # functions to print test results to log

import os # necessary for making a directory to save all test-related outputs
import requests
import subprocess
import unittest
import datetime
import timeit
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

# This test creates a folder whose name is dynamically generated, based on system time.
# Get the date formatted as year-mm-dd_hr:min.
timeOfTest = str(datetime.datetime.now()).replace(' ', '_').replace(':', '-')[0:16]
folderName = 'tempIDM'+timeOfTest
os.makedirs('./'+folderName)
logging.basicConfig(filename=folderName+'/'+timeOfTest + '_IDMtest.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


class IdmTest(unittest.TestCase):
    # Here are the class variables shared among all instances "self" of IdmTest
    ERRORCOLOR = "\u001b[31m" #red
    WARNINGCOLOR = "\u001b[33m" #yellow
    SUCCESSCOLOR = "\u001b[32m" #green
    DEFAULTCOLOR = "\u001b[0m" #white
    browser = None
    sites = None
    types = None
    browserType = None
    timeStart = None
    siteList = ['campusdirectory', 'cruzidmanager', 'grouper']
    # Ask the user which server and which browser they want to test
    while (types!='dev' and types!='stage' and types!='prod'):
        types = input("Enter the server you wish to test (dev or stage): ")
    while (browserType!='chrome' and browserType!='firefox'):
        browserType = input("Enter the browser you wish to test on (chrome or firefox): ")

# SETUP FUNCTIONS--------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super(IdmTest, self).__init__(*args, **kwargs)
        if self.browser is None:
            self.setupBrowser(self.browserType)
        if self.sites is None:
            self.sites = {}
            for site in self.siteList:
                self.setupSite(site)

    def __del__(self):
        #if self.timeStart is not None:
        #    timeElapsed = timeit.default_timer() - self.timeStart
        #    write_log.logSummary(self.browserType, timeElapsed)
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



# HELPER FUNCTIONS---------------------------------------------------------

    def setupBrowser(self, browserName):
        #self.browser = [] (used to be an array of browsers)
        if browserName=='firefox':
            try:
                driver = webdriver.Firefox()
                driver.implicitly_wait(30)
                self.browser = driver
            except:
                write_log.logSetupError("firefox")
                print("Unable to load firefox")
        else: # DEFAULT TO CHROME
            try:
                driver = webdriver.Chrome()
                driver.implicitly_wait(30)
                self.browser = driver
            except:
                write_log.logSetupError("chrome")
                print("Unable to load chrome")

    # TODO: Can destroy a credential after it's used in the test.
    # "frontloading" : grabbing all credentials in the beginning of the test.
    def setupSite(self, siteName):
        cred = return_credentials.get_item(siteName + "-cred")
        # assert(cred is not None)
        if self.types=='stage':
            site = {}
            site['url'] = (cred.url).replace("dev", "stg")
            site['username'] = cred.user
            site['password'] = cred.pw
            self.sites[siteName] = site
        # elif self.types=='prod'
        else: # default to self.types=='dev'
            site = {}
            site['url'] = cred.url
            site['username'] = cred.user
            site['password'] = cred.pw
            self.sites[siteName] = site


    # Checks that siteName's credentials actually exist in LastPass.
    def check_site_exists(self, siteName):
        assert(self.sites is not None)
        # Did the site information get mapped to our local python dict variable?
        try:
            site = self.sites[siteName]
            write_log.logInfoMsg("LastPass", siteName+" exists")
            print(self.SUCCESSCOLOR+siteName+" found in LastPass"+self.DEFAULTCOLOR)
            return True
        except:
            write_log.logSiteNotFound(siteName)
            print(self.ERRORCOLOR+"ERROR: "+siteName+" credentials not found in your LastPass account"+self.DEFAULTCOLOR)
            return False

    # Makes sure status code of a site is acceptable.
    def check_status(self, siteUrl):
        try:
            # time out after 2 minutes
            r = requests.get(siteUrl, timeout=121)
            if r.status_code!=200 and r.status_code!=301 and r.status_code!=302:
                write_log.logHttpError(siteUrl, r.status_code)
                print(self.ERRORCOLOR+"ERROR: "+siteUrl+" returns status code "+str(r.status_code)+self.DEFAULTCOLOR)
                return False
            else:
                write_log.logInfoMsg(siteUrl, "status code "+str(r.status_code))
                print(self.SUCCESSCOLOR+siteUrl+" returns status code "+str(r.status_code)+self.DEFAULTCOLOR)
                return r.status_code # site returns good status code and we can proceed with the webdriver test
        except:
            write_log.logTimeout(siteUrl, 2)
            print(self.ERRORCOLOR+"ERROR: "+siteUrl+" took over 2 minutes to load"+self.DEFAULTCOLOR)
            return False # requests.get() function timed out


    # Generic login function to a site
    def login(self, siteName):
        assert(self.browser is not None)
        assert(self.sites is not None)
        browser = self.browser
        site = self.sites[siteName]

        write_log.logInfoMsg(siteName, "login test started")
        print("Testing login")

        # Log in
        usernameBox = None
        passwordBox = None
        # Note: define variables outside of try block so scope is larger
        try:
            usernameBox = browser.find_element_by_xpath('//input[@type="text"]')
        except:
            write_log.logButtonMissing(site['url'], "Login field")
            print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+"could not locate login field")
            return False
        try:
            passwordBox = browser.find_element_by_xpath('//input[@type="password"]')
        except:
            write_log.logButtonMissing(site['url'], "Password field")
            print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+"could not locate password field")
            return False

        assert(usernameBox is not None)
        assert(passwordBox is not None)

        try:
            usernameBox.clear()
            usernameBox.send_keys(site['username'])
            passwordBox.clear()
            passwordBox.send_keys(site['password'])
            passwordBox.send_keys(Keys.ENTER)
            #return True
        except Exception as e:
            write_log.logErrorMsg(siteName, "Login failed")
            print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+"Login failed")
            browser.save_screenshot(folderName+'/error_logininput_idmtest.png')
            print(e)
            #raise(e)
            return False
        return True


    # Generic login verification function to a site
    def verify_logged_in(self, siteName, text):
        assert(self.browser is not None)
        assert(self.sites is not None)
        browser = self.browser
        site = self.sites[siteName]

        browser.implicitly_wait(30)

        if text not in browser.page_source and siteName=='cruzidmanager':
            usernameBox = None
            try:
                usernameBox = browser.find_element_by_id("txtCruzId")
                # Error 1: login failed, means still on original login page
                if usernameBox is not None:
                    write_log.logErrorMsg(siteName, "Log in failed")
                    print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+"Log in to "+siteName+" failed")
                    browser.save_screenshot(folderName+'/error_loginfailed_idmtest.png')
                    #TODO: print if screenshot was generated
                    return False
            except:
                # Error 2: usernameBox not found, means log in passed and next page fails to load
                write_log.logErrorMsg(browser.current_url, "Page fails to load after login")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+"Log Out " + site['username'] + " text missing after successful login")
                browser.save_screenshot(folderName+'/error_loginfailed_idmtest.png')
                return False
        elif text not in browser.page_source:
            write_log.logErrorMsg(siteName, "'"+text+"' missing after login")
            print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+siteName+" login failed")
            browser.save_screenshot(folderName+'/error_loginfailed_idmtest.png')
            return False

        assert(text in browser.page_source)
        write_log.logSuccess(siteName+'\n', "login")
        print(self.SUCCESSCOLOR+"PASSED:"+self.DEFAULTCOLOR+" login to "+siteName)
        return True

    # View the IDM Queue in cruzidmanager
    # Precondition: already logged in
    def view_idm_queue(self):
        assert(self.browser is not None)
        assert(self.sites is not None)
        browser = self.browser
        siteName = 'cruzidmanager'
        site = self.sites[siteName]
        write_log.logInfoMsg(siteName, "view idm queue test started")
        print("Testing view idm queue")
        try:
            # View IDM Queue
            enterAdmin = None
            try:
                enterAdmin = browser.find_element_by_link_text("CruzID Admin")
            except:
                write_log.logButtonMissing(browser.current_url, "CruzID Admin button")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" 'CruzID Admin' option not visible")
                browser.save_screenshot(folderName+'/error_adminmissing_idmtest.png')
                return False
            assert(enterAdmin is not None)
            enterAdmin.click()

            advancedButton = None
            try:
                advancedButton = browser.find_element_by_xpath("(//a[contains(text(),'Advanced')])[2]")
            except:
                write_log.logButtonMissing(browser.current_url, "'Advanced' button for Admin")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" 'Advanced' button for Admin missing")
                browser.save_screenshot(folderName+'/error_advancedmissing_idmtest.png')
                return False
            assert(advancedButton is not None)
            advancedButton.click()

            viewQueueButton = None
            try:
                viewQueueButton = browser.find_element_by_link_text("View IDM Queue")
            except:
                write_log.logButtonMissing(browser.current_url, "'View IDM Queue' button")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" 'View IDM Queue' button missing")
                browser.save_screenshot(folderName+'/error_viewqueuemissing_idmtest.png')
                return False
            assert(viewQueueButton is not None)
            viewQueueButton.click()

            browser.implicitly_wait(10)

            if "Provisioning queue" not in browser.page_source:
                write_log.logErrorMsg(browser.current_url+'\n', "Provisioning Queue missing")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" 'Provisioning queue' missing in IDM Queue page")
                browser.save_screenshot(folderName+'/error_queuemissing_idmtest.png')
            else:
                write_log.logSuccess(siteName+'\n', "login and load IDM Queue")
                print(self.SUCCESSCOLOR+"PASSED:"+self.DEFAULTCOLOR+" logged in and loaded IDM Queue page")
                browser.save_screenshot(folderName+'/success_idmqueue_idmtest.png')

            # EXIT Admin
            exitAdmin = None
            try:
                exitAdmin = browser.find_element_by_link_text("Exit Admin")
            except:
                write_log.logButtonMissing(browser.current_url, "'Exit Admin' button")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" missing the option to exit Admin view")
                browser.save_screenshot(folderName+'/error_exitadminmissing_idmtest.png')
                return False
            assert(exitAdmin is not None)
            exitAdmin.click()
            return True

        except Exception as e:
            print(e)
            return False
            # raise(e) Do not raise exception because you want to be able to continue to the next test


    # Create group function for cruzidmanager
    # Precondition: already logged in
    def create_group(self, siteName):
        assert(self.browser is not None)
        assert(self.sites is not None)
        browser = self.browser
        #siteName = 'cruzidmanager'
        site = self.sites[siteName]

        try:
            write_log.logInfoMsg(siteName, "group creation test started")
            print("Testing group creation")

            # Create group
            advancedButton = None
            try:
                advancedButton = browser.find_element_by_link_text("Advanced")
            except:
                write_log.logButtonMissing(browser.current_url, "'Advanced' option")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" 'Advanced' button for groups is missing")
                browser.save_screenshot(folderName+'/error_advancedoptionmissing_idmtest.png')
                return False
            assert(advancedButton is not None)
            advancedButton.click()

            groupButton = None
            try:
                groupButton = browser.find_element_by_link_text("Group Management")
            except:
                write_log.logButtonMissing(browser.current_url, "'Group Management' button")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" 'Group Management' button missing")
                browser.save_screenshot(folderName+'/error_groupmngment_idmtest.png')
                return False
            assert(groupButton is not None)
            groupButton.click()

            newGroup = None
            try:
                newGroup = browser.find_element_by_link_text("Add New Group")
            except:
                write_log.logButtonMissing(browser.current_url, "'Add New Group' button")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" 'Add New Group' button missing")
                browser.save_screenshot(folderName+'/error_addgroupmissing_idmtest.png')
                return False
            assert(newGroup is not None)
            newGroup.click()

            groupNameInput = None
            try:
                groupNameInput = browser.find_element_by_id("groupNameInput")
            except:
                write_log.logButtonMissing(browser.current_url, "'Input your group name' field missing")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" couldn't find field to input group name")
                browser.save_screenshot(folderName+'/error_groupnameinputmissing_idmtest.png')
                return False
            assert(groupNameInput is not None)
            groupNameInput.click()
            groupNameInput.clear()
            # Group name must be a unique string
            groupName = "AT"+str(datetime.datetime.now()).replace(" ", "").replace("-","")[:16]
            groupName = groupName.replace(":","")
            groupNameInput.send_keys(groupName)
            #print("group name is " + groupName)

            groupDescribe = None
            try:
                groupDescribe = browser.find_element_by_name("groupDescription")
            except:
                write_log.logButtonMissing(browser.current_url, "'Input group description' field missing")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" 'Group Description' field missing")
                browser.save_screenshot(folderName+'/error_groupdescriptionmissing_idmtest.png')
                return False
            assert(groupDescribe is not None)
            groupDescribe.clear()
            groupDescribe.send_keys("Automated test")

            submitButton = None
            try:
                submitButton = browser.find_element_by_id("submit")
            except:
                write_log.logButtonMissing(browser.current_url, "'Create Group' button")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" 'Create Group' button missing")
                browser.save_screenshot(folderName+'/error_creategroupmissing_idmtest.png')
                return False
            assert(submitButton is not None)
            submitButton.click()

            browser.implicitly_wait(10)

            if "The group was created." not in browser.page_source or "EXCEPTION" in browser.page_source:
                write_log.logErrorMsg(siteName+'\n', "Failed to create a group with name"+groupName)
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" failed to create new group with name " + groupName)
                browser.save_screenshot(folderName+'/error_creategroup_idmtest.png')
                return False
            else:
                write_log.logSuccess(siteName+'\n', "logged in and created group "+groupName)
                print(self.SUCCESSCOLOR+"PASSED:"+self.DEFAULTCOLOR+" new group \u001b[32m" + groupName + "\u001b[0m created")
                browser.save_screenshot(folderName+'/success_creategroup_idmtest.png')
                return True
        except Exception as e:
            print(e)
            #raise(e)
            return False


    # Create sundry account for cruzidmanager
    # Precondition: already logged in
    def create_sundry(self, siteName):
        assert(self.browser is not None)
        assert(self.sites is not None)
        browser = self.browser
        site = self.sites[siteName]

        try:
            write_log.logInfoMsg(siteName, "sundry creation test started")
            print("Testing sundry creation")
            # Create sundry
            enterAdmin = None
            try:
                enterAdmin = browser.find_element_by_link_text("CruzID Admin")
            except:
                write_log.logButtonMissing(browser.current_url, "CruzID Admin button")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" missing 'CruzID Admin' option\n")
                return False
            assert(enterAdmin is not None)
            enterAdmin.click()

            advancedButton = None
            try:
                advancedButton = browser.find_element_by_xpath("(//a[contains(text(),'Advanced')])[2]")
            except:
                write_log.logButtonMissing(browser.current_url, "'Advanced' button for Admin")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" missing 'Advanced' button for Admin\n")
                return False
            assert(advancedButton is not None)
            advancedButton.click()

            sundryButton = None
            try:
                sundryButton = browser.find_element_by_link_text("Sundry")
            except:
                write_log.logButtonMissing(browser.current_url, "'Sundry' button")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" missing 'Sundry' button\n")
                browser.save_screenshot(folderName+'/error_sundrymissing_idmtest.png')
                return False
            assert(sundryButton is not None)
            sundryButton.click()

            sponsorButton = None
            try:
                sponsorButton = browser.find_element_by_id("sponsor")
            except:
                write_log.logButtonMissing(browser.current_url, "'sponsor' button for sundry creation")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" missing 'sponsor' button\n")
                browser.save_screenshot(folderName+'/error_sundrysponsormissing_idmtest.png')
                return False
            assert(sponsorButton is not None)
            sponsorButton.send_keys(site['username'])

            firstName = None
            try:
                firstName = browser.find_element_by_id("edit-first")
            except:
                write_log.logButtonMissing(browser.current_url, "Input first name field")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" missing 'First Name' field\n")
                browser.save_screenshot(folderName+'/error_sundryfirstnamemissing_idmtest.png')
                return False
            assert(firstName is not None)
            firstName.send_keys("Automated")

            lastName = None
            try:
                lastName = browser.find_element_by_id("edit-last")
            except:
                write_log.logButtonMissing(browser.current_url, "Input last name field")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" missing 'Last Name' field\n")
                browser.save_screenshot(folderName+'/error_sundrylastnamemissing_idmtest.png')
                return False
            assert(lastName is not None)
            lastName.send_keys("Testcase")

            birthDate = None
            try:
                birthDate = browser.find_element_by_id("birthdate")
            except:
                write_log.logButtonMissing(browser.current_url, "Input birthdate field")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" missing 'Date of Birth' field\n")
                browser.save_screenshot(folderName+'/error_sundrydobmissing_idmtest.png')
                return False
            assert(birthDate is not None)
            birthDate.send_keys("1/1/1980")

            sundryStatus = None
            try:
                sundryStatus = Select(browser.find_element_by_id("status"))
            except:
                write_log.logButtonMissing(browser.current_url, "sundry status field")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" missing 'Sundry Status' field\n")
                browser.save_screenshot(folderName+'/error_sundrystatusmissing_idmtest.png')
                return False
            assert(sundryStatus is not None)
            sundryStatus.select_by_visible_text("Staged")

            stagedOption = None
            try:
                stagedOption = browser.find_element_by_xpath("//option[@value='Staged']")
            except:
                write_log.logButtonMissing(browser.current_url, "staged option for sundry status")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" missing 'staged' option for sundry status\n")
                browser.save_screenshot(folderName+'/error_sundrystagedmissing_idmtest.png')
                return False
            assert(stagedOption is not None)
            stagedOption.click()

            expirationDate = None
            try:
                expirationDate = browser.find_element_by_id("datepicker")
            except:
                write_log.logButtonMissing(browser.current_url, "Input account expiration date field")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" missing Account 'Expiration Date' field\n")
                browser.save_screenshot(folderName+'/error_sundryexpirationmissing_idmtest.png')
                return False
            assert(expirationDate is not None)

            # Sundry test account will expire in one year
            sysTime = str(datetime.datetime.now())
            if sysTime[5:10]=='02-29': # leap year case
                mmdd = '03/01'
            else: # general case
                mmdd = sysTime[5:10].replace("-","/")
            yr = int(sysTime[:4]) + 1
            expirDate = mmdd + "/" + str(yr)
            expirationDate.send_keys(expirDate)
            #print("expires on " + expirDate)

            # Simulate mouse highlight text to give Sundry user two resources
            blueOption = None
            try:
                blueOption = browser.find_element_by_xpath("//option[@value='CruzIdBlue']")
            except:
                write_log.logButtonMissing(browser.current_url, "Option for CruzIdBlue")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" missing CruzIdBlue option\n")
                browser.save_screenshot(folderName+'/error_sundrybluemissing_idmtest.png')
                return False
            assert(blueOption is not None)
            goldOption = None
            try:
                goldOption = browser.find_element_by_xpath("//option[@value='CruzIdGold']")
            except:
                write_log.logButtonMissing(browser.current_url, "Option for CruzIdGold")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" missing CruzIdGold option\n")
                browser.save_screenshot(folderName+'/error_sundrygoldmissing_idmtest.png')
                return False
            assert(goldOption is not None)

            # drag_and_drop simulates a multiple-element highlight
            action = ActionChains(browser).drag_and_drop(blueOption, goldOption)
            action.perform()

            commentField = None
            try:
                commentField = browser.find_element_by_id("edit-comments")
            except:
                write_log.logButtonMissing(browser.current_url, "Input comments field")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" missing 'Comment' field\n")
                browser.save_screenshot(folderName+'/error_sundrycommentmissing_idmtest.png')
                return False
            assert(commentField is not None)
            commentField.send_keys("This is an automated test")

            submitButton = None
            try:
                submitButton = browser.find_element_by_id("edit-submit")
            except:
                write_log.logButtonMissing(browser.current_url, "'Create User' button")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" missing 'Create User' button\n")
                browser.save_screenshot(folderName+'/error_sundrycreatemissing_idmtest.png')
                return False
            assert(submitButton is not None)
            submitButton.click()

            browser.implicitly_wait(20)

            if "Sundry user created" not in browser.page_source:
                write_log.logErrorMsg(siteName+'\n', "Failed to create sundry account")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" failed to create sundry account\n")
                browser.save_screenshot(folderName+'/error_sundrycreation_idmtest.png')
                return False
            else:
                text = "Sundry user created with userID "
                index = browser.page_source.index(text) + len(text)
                newId = browser.page_source[index:index+8]
                write_log.logSuccess(siteName+'\n', "logged in and created sundry, ID "+newId+", expires "+expirDate)
                print(self.SUCCESSCOLOR+"PASSED:"+self.DEFAULTCOLOR+" created sundry account with userID"+self.SUCCESSCOLOR+newId+self.DEFAULTCOLOR+"\n        expires on " + expirDate + "\n")
                browser.save_screenshot(folderName+'/success_sundrycreation_idmtest.png')
                return True

        except Exception as e:
            print(e)
            #raise(e)

# TEST FUNCTIONS-------------------------------------------------------------------

    # Note: campusdirectory requires no login.
    # Verify that Admissions Office Information appears in a Campus Directory search.
    def test_campus_directory(self):
        assert(self.browser is not None)
        assert(self.sites is not None)
        # Make a shortcut for the class variable
        browser = self.browser
        siteName = 'campusdirectory'

        # Call helper function
        result1 = self.check_site_exists(siteName)
        if result1==False:
            print(self.ERRORCOLOR+"FAIL:"+self.DEFAULTCOLOR+" Test terminated prematurely. You need access to "+siteName+" url on LastPass.\n")
            write_log.logErrorMsg("LastPass.", "Test terminated. Url for "+siteName+" not found")
            return # exit test early
        # unnecessary to do: assert(result1==True)
        site = self.sites[siteName]

        # Call helper function
       #for debugging purposes- print(site['url'])
        result2 = self.check_status(site['url'])
        if result2==False:
            print(self.ERRORCOLOR+"FAIL:"+self.DEFAULTCOLOR+" Test terminated prematurely. "+site['url']+" unable to return acceptable status code.\n")
            write_log.logErrorMsg(site['url'], "Test terminated. Bad status code")
            return # exit test


        # Begin webdriver test after check_site_exists() and check_status() pass
        try:
            browser.get(site['url'])
            write_log.logStart(site['url'])
            print("Testing " + site['url'])

            # Locate department tab
            departmentTab = None
            if self.types=='stage':
                try:
                    departmentTab = browser.find_element_by_id("ui-id-2")
                except:
                    write_log.logButtonMissing(site['url'], "Department Tab Button")
                    print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+"Department Tab not found on "+self.ERRORCOLOR+site['url']+'\n'+self.DEFAULTCOLOR)
                    browser.save_screenshot(folderName+'/error_cd_idmtest.png')
                    #return
            else: # default to dev test
                try:
                    departmentTab = browser.find_element_by_xpath("//a[@id='departments']/span")
                except:
                    write_log.logButtonMissing(site['url'], "Department Tab Button")
                    print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+"Department Tab not found on "+self.ERRORCOLOR+site['url']+'\n'+self.DEFAULTCOLOR)
                    browser.save_screenshot(folderName+'/error_cd_idmtest.png')
                    #return
                    #print(e) #raise e
            if departmentTab==None:
                return
            departmentTab.click()
            # Locate the department dropdown list
            dropDown = None
            try:
                dropDown = browser.find_element_by_xpath("//div[@id='ucscpersonpubdepartmentnumber_chosen']/a/span")
            except:
                write_log.logButtonMissing(browser.current_url, "Department Dropdown Button")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" Department Dropdown not found\n")
                browser.save_screenshot(folderName+'/error_cdirectorydropdown_idmtest.png')
            if dropDown==None:
                return
            dropDown.click()
            # Find admissions office in the dropdown list
            browser.find_element_by_xpath("(//input[@type='text'])[3]").clear()
            browser.find_element_by_xpath("(//input[@type='text'])[3]").send_keys("admissions")
            browser.find_element_by_xpath("(//input[@type='text'])[3]").send_keys(Keys.ENTER)
            searchButton = None
            try:
                searchButton = browser.find_element_by_xpath("(//input[@value='Search directory'])[2]")
            except:
                write_log.logButtonMissing(browser.current_url, "Search Directory Button")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" 'Search Directory' button not found\n")
                browser.save_screenshot(folderName+'/error_searchdirectory_idmtest.png')
            if searchButton==None:
                return
            searchButton.click()

            browser.implicitly_wait(10)

            if "Department Web Site" not in browser.page_source or "831-459-2131" not in browser.page_source or "admissions@ucsc.edu" not in browser.page_source:
                write_log.logErrorMsg(browser.current_url+'\n', "Search for Admissions Office failed")
                print(self.ERRORCOLOR+"ERROR: "+self.DEFAULTCOLOR+" Admissions Office Department Information missing\n")
                browser.save_screenshot(folderName+'/error_officeinfo_idmtest.png')
            assert("831-459-2131" in browser.page_source)
            write_log.logSuccess(siteName+'\n', "search department")
            print(self.SUCCESSCOLOR+"PASSED:"+self.DEFAULTCOLOR+" search for Admissions Office Info in Campus Directory\n")
            browser.save_screenshot(folderName+'/success_cdsearch_idmtest.png')
            browser.close()

        except Exception as e:
            print(e)
            raise(e)


    # Log in, create group, access Admin Account, create Sundry, view IDM Queue in CruzID Manager.
    def test_cruzid_manager(self):
        assert(self.browser is not None)
        assert(self.sites is not None)
        browser = self.browser
        siteName = 'cruzidmanager'
        # Call helper function
        result1 = self.check_site_exists(siteName)
        if result1==False:
            print(self.ERRORCOLOR+"FAIL:"+self.DEFAULTCOLOR+" Test terminated prematurely. You need access to "+siteName+" credentials on LastPass.\n")
            write_log.logErrorMsg("LastPass.", "Test terminated. Credentials to "+siteName+" not found")
            return # exit test early
        # unnecessary to do: assert(result1==True)
        site = self.sites[siteName]

        # Call helper function
        result2 = self.check_status(site['url'])
        if result2==False:
            print(self.ERRORCOLOR+"FAIL:"+self.DEFAULTCOLOR+" Test terminated prematurely. "+site['url']+" unable to return acceptable status code.\n")
            write_log.logErrorMsg(site['url'], "Test terminated. Bad status code")
            return # exit test

        # Begin webdriver test after check_site_exists() and check_status() pass
        try:
            browser.get(site['url'])
            write_log.logStart(site['url'])
        except Exception as e:
            print(e)
            raise(e)

        print("Testing " + site['url'])

        # call test functions
        result = self.login('cruzidmanager')
        if result==False:
            print(self.ERRORCOLOR+"FAIL:"+self.DEFAULTCOLOR+" Test terminated prematurely. Login failed.\n")
            write_log.logErrorMsg(siteName, "Test terminated. Login failed")
            browser.close()
            return

        result = self.verify_logged_in('cruzidmanager', "Log Out " + site['username'])
        if result==False:
            print(self.ERRORCOLOR+"FAIL:"+self.DEFAULTCOLOR+" Test terminated prematurely. Login success page failed to load.\n")
            write_log.logErrorMsg(siteName, "Test terminated. Login success page failed to load")
            browser.close()
            return

        self.view_idm_queue()
        self.create_group('cruzidmanager')
        self.create_sundry('cruzidmanager')
        browser.close()


    # Verify that the login feature works in Grouper.
    def test_grouper(self):
        assert(self.browser is not None)
        assert(self.sites is not None)
        browser = self.browser
        siteName = 'grouper'

        # Call helper function
        result1 = self.check_site_exists(siteName)
        if result1==False:
            print(self.ERRORCOLOR+"FAIL:"+self.DEFAULTCOLOR+" Test terminated prematurely. You need access to "+siteName+" credentials on LastPass.\n")
            write_log.logErrorMsg("LastPass.", "Test terminated. Credentials to "+siteName+" not found")
            return
        # unnecessary to do: assert(result1==True)
        site = self.sites[siteName]

        # Call helper function
        result2 = self.check_status(site['url'])
        if result2==False:
            print(self.ERRORCOLOR+"FAIL:"+self.DEFAULTCOLOR+" Test terminated prematurely. "+site['url']+" unable to return acceptable status code.\n")
            write_log.logErrorMsg(site['url'], "Test terminated. Bad status code")
            return # exit test

        # Begin webdriver test after check_site_exists() and check_status() pass
        try:
            browser.get(site['url'])
            write_log.logStart(site['url'])
        except Exception as e:
            print(e)
            raise(e)

        print("Testing " + site['url'])

        # Call test function
        result = self.login('grouper')
        if result==False:
            print(self.ERRORCOLOR+"FAIL:"+self.DEFAULTCOLOR+" Test terminated prematurely. Login failed.\n")
            write_log.logErrorMsg(siteName, "Test terminated. Login failed")
            browser.close()
            return
        browser.implicitly_wait(30)
        result = self.verify_logged_in('grouper', 'Logged in as')
        if result==False:
            print(self.ERRORCOLOR+"FAIL:"+self.DEFAULTCOLOR+" Test terminated prematurely. Login success page failed to load.\n")
            write_log.logErrorMsg(siteName, "Test terminated. Login success page failed to load")
            browser.close()
            return

        logoutButton = None
        try:
            logoutButton = browser.find_element_by_link_text("Log out")
        except:
            write_log.logButtonMissing(browser.current_url, "Logout element")
            print(self.WARNINGCOLOR+"Warning:"+self.DEFAULTCOLOR+" could not locate logout element on "+self.WARNINGCOLOR+browser.current_url+self.DEFAULTCOLOR)


if __name__ == "__main__":
    username = ""
    while "@ucsc.edu" not in username:
        username = input("Enter LastPass username (Make sure to include @ucsc.edu): ")
    # Use python's subprocess module to log user into lastpass
    subprocess.call(['lpass', 'login', username])
    print("\n\u001b[33mAll test logs and screenshots will be saved to the following folder in your current directory:\n" + folderName + "\n\u001b[0m")
    # unittest.main() calls the init, setup, teardown, del, and all functions beginning with the string "test" in the above class
    unittest.main()
