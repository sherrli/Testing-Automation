#!/usr/local/bin/python
# coding=utf-8


intro="""
----------------------------------------------------------------
Name        : Login Test
Description : Verify pages have correct content on dev sites.
Author      : shli17
File        : ches-login.py
----------------------------------------------------------------
"""
print(intro)

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import json
import time


class ches_login_test(unittest.TestCase):
    browsers = None
    pwsites = None
    bdsites = None


    def __init__(self, *args, **kwargs):
        super(ches_login_test, self).__init__(*args, **kwargs)
        if self.browsers is None:
            self.setupBrowsers()
        if self.pwsites is None:
            self.setupPwSites()
        if self.bdsites is None:
            self.setupBdSites()

    def __del__(self):
        if self.browsers is not None:
            for browser in self.browsers:
                try:
                    browser.close()
                    browser.quit()
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


    def setupPwSites(self):
        # use json credentials file
        with open(os.getcwd() + '/ches-login-pw.json') as data_file:
            data = json.load(data_file)
            self.pwsites = {}
            for siteData in data['credentials']:
                site = {}
                site['dev_url'] = siteData['dev_url']
                site['id'] = siteData['id']
                site['password'] = siteData['password']
                self.pwsites[siteData['siteName']] = site

    def setupBdSites(self):
        # use json credentials file
        with open(os.getcwd() + '/ches-login-bd.json') as data_file:
            data = json.load(data_file)
            self.bdsites = {}
            for siteData in data['credentials']:
                site = {}
                site['dev_url'] = siteData['dev_url']
                site['id'] = siteData['id']
                site['mm'] = siteData['mm']
                site['dd'] = siteData['dd']
                site['yr'] = siteData['yr']
                self.bdsites[siteData['siteName']] = site


    def setupBrowsers(self):
        self.browsers=[]

        try:
            chrome = webdriver.Chrome() #search path
            #chrome = webdriver.Chrome('/usr/local/bin/chromedriver')
            chrome.implicitly_wait(30)
            self.browsers.append(chrome)

        except:
            print("Unable to load chrome")
#         webdriver.DesiredCapabilities.
#         webdriver.DesiredCapabilities.ANDROID
#         webdriver.DesiredCapabilities.EDGE
#         webdriver.DesiredCapabilities.OPERA
#         webdriver.DesiredCapabilities.IPAD


    def test_careercentersecure_hrstaff(self):
        self.careercenter_staff_test("careercentersecure-hrstaff")

    def test_careercentersecure_staff(self):
        self.careercenter_staff_test("careercentersecure-staff")

    def test_careercentersecure_student1(self):
        self.careercenter_student_test("careercentersecure-student1")

    def test_careercentersecure_student2(self):
        self.careercenter_student_test("careercentersecure-student2")

    def test_careercentersecure_student3(self):
        self.careercenter_student_test("careercentersecure-student3")

    def test_careercentersecure_supervisor(self):
        self.careercenter_staff_test("careercentersecure-supervisor")

    def test_eopotss_admin(self):
        self.eopotss_admin_test("eop-otss-admin")

    def test_eopotss_msi(self):
        self.eopotss_msi_test("eop-otss-msi")

    def test_eopotss_staff(self):
        self.eopotss_staff_test("eop-otss-staff")

    def test_eopotss_student(self):
        self.eopotss_student_test("eop-otss-student")

    def test_eopotss_tutor(self):
        self.eopotss_tutor_test("eop-otss-tutor")

    def test_fixit(self):
        self.fixit_test("fixit")


    def careercenter_staff_test(self,siteName):
        assert(self.browsers is not None)
        assert(self.pwsites is not None)
        text = "Work-study Information"
        for browser in self.browsers:
            try:
                site = self.pwsites[siteName]
                if not site:
                    print("Could not find %s")
                browser.get(site['dev_url'])
                print("Testing " + site['dev_url'])

                self.username = site['id']
                self.password = site['password']
                username_txt = browser.find_element_by_name("logon")
                password_txt = browser.find_element_by_name("pass")
                assert(username_txt is not None)
                assert(password_txt is not None)

                username_txt.clear()
                username_txt.send_keys(self.username)
                password_txt.clear()
                password_txt.send_keys(self.password)
                browser.find_element_by_name("pass").send_keys(Keys.ENTER) # submit button not visible

                if text not in browser.page_source:
                    print("ERROR: " + text + " not in " + siteName + " source after successful login\n")
                assert(text in browser.page_source)

                logout_txt = browser.find_element_by_xpath("//area")
                assert(logout_txt is not None)
                logout_txt.click()
                print("PASS: %s using %s\n" % (siteName,browser.name.capitalize()))

            except Exception as e:
                print(e)
                raise e
            finally:
                browser.close()


    def careercenter_student_test(self,siteName):
        assert(self.browsers is not None)
        assert(self.pwsites is not None)
        for browser in self.browsers:
            try:
                site = self.pwsites[siteName]
                if not site:
                    print("Could not find %s")
                browser.get(site['dev_url'])
                print("Testing " + site['dev_url'])

                self.username = site['id']
                self.password = site['password']
                username_txt = browser.find_element_by_name("SID")
                password_txt = browser.find_element_by_name("birthdate")

                assert(username_txt is not None)
                assert(password_txt is not None)

                username_txt.clear()
                username_txt.send_keys(self.username)
                password_txt.clear()
                password_txt.send_keys(self.password)
                # log in:
                browser.find_element_by_name("birthdate").send_keys(Keys.ENTER)
                # TODO: test if the continue links are working
                # browser.find_element_by_name("action").click()
                # log out:
                browser.find_element_by_xpath("//area").click()
                print("PASS: %s using %s\n" % (siteName,browser.name.capitalize()))

            except Exception as e:
                print(e)
                raise e
            finally:
                browser.close()

    def eopotss_admin_test(self,siteName):
        assert(self.browsers is not None)
        assert(self.pwsites is not None)
        text = "System lockout options"
        for browser in self.browsers:
            try:
                site = self.pwsites[siteName]
                if not site:
                    print("Could not find %s")
                browser.get(site['dev_url'])
                print("Testing " + site['dev_url'])

                self.username = site['id']
                self.password = site['password']

                username_txt = browser.find_element_by_name('username')
                password_txt = browser.find_element_by_name('password')
                submit_txt = browser.find_element_by_name('signinform')
                assert(username_txt is not None)
                assert(password_txt is not None)
                assert(submit_txt is not None)

                username_txt.clear()
                username_txt.send_keys(self.username)
                password_txt.clear()
                password_txt.send_keys(self.password)
                submit_txt.submit()

                if text not in browser.page_source:
                    print("ERROR: " + text + " not in " + siteName + " source after successful login\n")
                assert(text in browser.page_source)

                logout_txt = browser.find_element_by_xpath("//a[contains(text(),'Click\n                  here to logout')]")
                assert(logout_txt is not None)
                logout_txt.click()
                print("PASS: %s using %s\n" % (siteName,browser.name.capitalize()))

            except Exception as e:
                print(e)
                raise e
            finally:
                browser.close()


    def eopotss_staff_test(self,siteName):
        assert(self.browsers is not None)
        assert(self.pwsites is not None)
        title = "UCSC Learning Support Services On-line Tutor Signup System"
        for browser in self.browsers:
            try:
                site = self.pwsites[siteName]
                if not site:
                    print("Could not find %s")
                browser.get(site['dev_url'])
                print("Testing " + site['dev_url'])

                self.username = site['id']
                self.password = site['password']

                username_txt = browser.find_element_by_name('username')
                password_txt = browser.find_element_by_name('password')
                submit_txt = browser.find_element_by_name('Submit')
                assert(username_txt is not None)
                assert(password_txt is not None)
                assert(submit_txt is not None)

                username_txt.clear()
                username_txt.send_keys(self.username)
                password_txt.clear()
                password_txt.send_keys(self.password)
                submit_txt.click()

                if title not in browser.title:
                    print("ERROR: " + title + " not in " + siteName + " after successful login\n")
                assert(title in browser.title)

                logout_txt = browser.find_element_by_link_text("Logout")
                assert(logout_txt is not None)
                logout_txt.click()

                print("PASS: %s using %s\n" % (siteName,browser.name.capitalize()))

            except Exception as e:
                print(e)
                raise e
            finally:
                browser.close()


    def eopotss_msi_test(self,siteName):
        assert(self.browsers is not None)
        assert(self.bdsites is not None)
        text = "Account Options"
        for browser in self.browsers:
            try:
                site = self.bdsites[siteName]
                if not site:
                    print("Could not find %s")
                browser.get(site['dev_url'])
                print("Testing " + site['dev_url'])

                self.username = site['id']
                self.mm = site['mm']
                self.dd = site['dd']
                self.yr = site['yr']

                username_txt = browser.find_element_by_name('SID')
                password_mm = browser.find_element_by_id('BDayMM')
                password_dd = browser.find_element_by_id('BDayDD')
                password_yr = browser.find_element_by_id('BDayYR')
                submit_txt = browser.find_element_by_name('Submit')
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

                logout_txt = browser.find_element_by_name('logout')
                assert(logout_txt is not None)
                logout_txt.click()
                print("PASS: %s using %s\n" % (siteName,browser.name.capitalize()))

            except Exception as e:
                print(e)
                raise e
            finally:
                browser.close()


    def eopotss_student_test(self,siteName):
        # tutor and student tests require separate registration
        assert(self.browsers is not None)
        assert(self.bdsites is not None)
        text = "registration"
        # the student account has not been registered for access
        # "please go to our registration site to continue" text appears
        for browser in self.browsers:
            try:
                site = self.bdsites[siteName]
                if not site:
                    print("Could not find %s")
                browser.get(site['dev_url'])
                print("Testing " + site['dev_url'])

                self.username = site['id']
                self.mm = site['mm']
                self.dd = site['dd']
                self.yr = site['yr']

                username_txt = browser.find_element_by_name('SID')
                password_mm = browser.find_element_by_id('BDayMM')
                password_dd = browser.find_element_by_id('BDayDD')
                password_yr = browser.find_element_by_id('BDayYR')
                submit_txt = browser.find_element_by_name('signinform')
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
                submit_txt.submit() #try .click() also

                if text not in browser.page_source:
                    print("ERROR: " + text + " not in " + siteName + " source after successful login\n")
                assert(text in browser.page_source)

                print("PASS: %s using %s\n" % (siteName,browser.name.capitalize()))

            except Exception as e:
                print(e)
                raise e
            finally:
                browser.close()

    def eopotss_tutor_test(self,siteName):
        # tutor and student tests require separate registration
        assert(self.browsers is not None)
        assert(self.bdsites is not None)
        text = "closed" # the tutor site is closed during summer?
        for browser in self.browsers:
            try:
                site = self.bdsites[siteName]
                if not site:
                    print("Could not find %s")
                browser.get(site['dev_url'])
                print("Testing " + site['dev_url'])

                self.username = site['id']
                self.mm = site['mm']
                self.dd = site['dd']
                self.yr = site['yr']

                username_txt = browser.find_element_by_name('SID')
                password_mm = browser.find_element_by_id('BDayMM')
                password_dd = browser.find_element_by_id('BDayDD')
                password_yr = browser.find_element_by_id('BDayYR')
                submit_txt = browser.find_element_by_name('LOGIN')
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
                submit_txt.submit() #try .click() also

                if text not in browser.page_source:
                    print("ERROR: " + text + " not in " + siteName + " source after successful login\n")
                assert(text in browser.page_source)

                print("PASS: %s using %s\n" % (siteName,browser.name.capitalize()))

            except Exception as e:
                print(e)
                raise e
            finally:
                browser.close()

#TODO: check the page for presence of a header or something
    def fixit_test(self,siteName):
        assert(self.browsers is not None)
        assert(self.pwsites is not None)
        text = "Location of Problem"
        # TODO: FIXIT-DEV has no LOGOUT option
        for browser in self.browsers:
            try:
                site = self.pwsites[siteName]
                if not site:
                    print("Could not find %s")
                browser.get(site['dev_url'])
                print("Testing " + site['dev_url'])

                self.username = site['id']
                self.password = site['password']

                username_txt = browser.find_element_by_id("enteremail")
                password_txt = browser.find_element_by_id("enterpassword")
                submit_txt = browser.find_element_by_xpath("//img[@alt='Student']")
                assert(username_txt is not None)
                assert(password_txt is not None)
                assert(submit_txt is not None)

                username_txt.clear()
                username_txt.send_keys(self.username)
                password_txt.clear()
                password_txt.send_keys(self.password)
                submit_txt.click()

                if text not in browser.page_source:
                    print("ERROR: " + text + " not in " + siteName + " source after successful login\n")
                assert(text in browser.page_source)

                print("PASS: %s using %s\n" % (siteName,browser.name.capitalize()))

            except Exception as e:
                print(e)
                raise e
            finally:
                browser.close()

# TODO: Verify that logout buttons actually work

if __name__ == "__main__":
    unittest.main()
