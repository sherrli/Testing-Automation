# coding=utf-8

from selenium import webdriver
from xvfbwrapper import Xvfb
import unittest
import os
import sys
sys.path.append("..")
import json
import datetime
import timeit
import check_status
import spreadsheet

class LampDevTest(unittest.TestCase):
    json_file = "sites-lamp.json"
    browser = None
    sites = None
    today = str(datetime.datetime.now())

    def __init__(self, *args, **kwargs):
        super(LampDevTest, self).__init__(*args, **kwargs)
        if self.sites is None:
            self.setupSites()
        # Initialize a spreadsheet object
        self.spreadsheet = spreadsheet.Spreadsheet()
        self.spreadsheet.open_sheet(str(type(self).__name__))
        self.next_row = self.spreadsheet.next_available_row()

    def __del__(self):
        if self.browser is not None:
            try:
                self.browser.quit()
                del self.spreadsheet
            except Exception as e:
                print(e)


    def setupSites(self):
        with open(os.getcwd() + '/' + self.json_file) as data_file:
            data = json.load(data_file)
                    # save the json information into a dictionary
                    # 'with' command automatically closes data_file
                    #for k,v in data.items():
                    #	print(k)
                    #	print(v)
            self.sites = {}
            for siteData in data['sites']:
                site = {}
                site['url'] = siteData['url']
                site['title'] = siteData['title']
                self.sites[siteData['siteName']] = site
                # data is of type dict

# TEST FUNCTIONS------------------------------------

    def test_its(self):
        self.run_test('its',self.next_row)

    def test_itsserverstatus(self):
        self.run_test('itsserverstatus',self.next_row+1)

    def test_itsmeminfo(self):
        self.run_test('itsmeminfo',self.next_row+2)

    def test_its9002(self):
        self.run_test('its9002',self.next_row+3)

    def test_its9004(self):
        self.run_test('its9004',self.next_row+4)

    def test_corgrants(self):
        self.run_test('corgrants',self.next_row+5)

    def test_cars(self):
        self.run_test('cars',self.next_row+6)

    def test_donatemeals(self):
        self.run_test('donatemeals',self.next_row+7)

    def test_discreet(self):
        self.run_test('discreet',self.next_row+8)

    def test_webapps(self):
        self.run_test('webapps',self.next_row+9)

    def test_webappswcms(self):
        self.run_test('webappswcms',self.next_row+10)

    def test_lamp9004(self):
        self.run_test('lamp9004',self.next_row+11)

    def test_lamp9004wcms(self):
        self.run_test('lamp9004wcms',self.next_row+12)

    def test_mobile(self):
        self.run_test('mobile',self.next_row+13)


    # HELPER FUNCTION----------------------------
    def run_test(self, siteName, row):
        with Xvfb() as xvfb:
            try:
                driver = webdriver.Firefox()
                driver.implicitly_wait(30)
                self.browser = driver
            except:
                print("Unable to load firefox in virtual display")
                assert(self.browser is not None)
                assert(self.sites is not None)
                browser = self.browser
            try:
                site = self.sites[siteName]
                # Populate spreadsheet with app name, class name, current date.
                self.spreadsheet.write_cell(row,1,siteName)
                self.spreadsheet.write_cell(row,2,type(self).__name__)
                self.spreadsheet.write_cell(row,3,self.today[:16])

                # Verify HTTP status code
                result = check_status.checkStatus(site['url'], [200, 301, 302])
                if result==False:
                    self.spreadsheet.write_cell(row,5,"fail\ninvalid http response")
                    return

                browser.get(site['url'])
                print("Testing " + site['url'])
                if site['title'] not in browser.title:
                    print("ERROR: " + site['title'] + " not in " + browser.title)
                    self.spreadsheet.write_cell(row,5,"fail")
                    #assert(site['title'] in browser.title)
                else:
                    self.spreadsheet.write_cell(row,5,"pass")
                    #print("PASS: %s using %s" % (siteName, browser.name.capitalize()))
            except Exception as e:
                print(e)
                #raise e


if __name__ == "__main__":
    unittest.main()
