# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class otss_test(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://eop.sa-stage.ucsc.edu/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_otss(self):
        driver = self.driver
        driver.get(self.base_url + "/OTSS/lcadmin/")

        driver.find_element_by_name("username").clear()
        driver.find_element_by_name("username").send_keys("pwaugh")
        driver.find_element_by_name("password").clear()
        driver.find_element_by_name("password").send_keys("phil")
        driver.find_element_by_name("Submit").click()
        driver.find_element_by_link_text("System lockout options").click()
        driver.find_element_by_name("Submit").click()
        driver.find_element_by_link_text("Click here to return to the main menu.").click()
        driver.find_element_by_link_text("Spring 2016").click()
        driver.find_element_by_name("Submit").click()
#         driver.find_element_by_link_text("Click here to return to the main menu.").click()
#         driver.find_element_by_link_text("Click here to return to the main menu.").click()
#         driver.find_element_by_link_text("1 waitlist requests").click()
#         driver.find_element_by_link_text("1 waitlist requests").click()
#         driver.find_element_by_link_text("Lau,Calvin Wing-Yin").click()
#         driver.find_element_by_link_text("Lau,Calvin Wing-Yin").click()
#         driver.find_element_by_id("comments").clear()
#         driver.find_element_by_id("comments").send_keys("test")
#         driver.find_element_by_id("comments").clear()
#         driver.find_element_by_id("comments").send_keys("test")
#         driver.find_element_by_css_selector("font > input[name=\"Submit\"]").click()
#         driver.find_element_by_css_selector("font > input[name=\"Submit\"]").click()
#         driver.find_element_by_link_text("Click here to return to the main menu.").click()
#         driver.find_element_by_link_text("Click here to return to the main menu.").click()
#         driver.find_element_by_link_text("Add/Modify announcements to the system").click()
#         driver.find_element_by_link_text("Add/Modify announcements to the system").click()
#         driver.find_element_by_name("Submit").click()
#         driver.find_element_by_name("Submit").click()
#         driver.find_element_by_link_text("Click here to return to the main menu.").click()
#         driver.find_element_by_link_text("Click here to return to the main menu.").click()
#         driver.find_element_by_link_text("Add/Modify messages").click()
#         driver.find_element_by_link_text("Add/Modify messages").click()
#         driver.find_element_by_id("submit1").click()
#         driver.find_element_by_id("submit1").click()
#         driver.find_element_by_link_text("Click here to return to the main menu.").click()
#         driver.find_element_by_link_text("Click here to return to the main menu.").click()
#         driver.find_element_by_link_text("Search for available tutoring sessions").click()
#         driver.find_element_by_link_text("Search for available tutoring sessions").click()
#         driver.find_element_by_link_text("Subject Tutoring").click()
#         driver.find_element_by_link_text("Subject Tutoring").click()
#         driver.find_element_by_name("Submit").click()
#         driver.find_element_by_name("Submit").click()
#         driver.find_element_by_link_text("Click here to return to the main menu.").click()
#         driver.find_element_by_link_text("Click here to return to the main menu.").click()
#         driver.find_element_by_link_text("Set quarter info in system").click()
#         driver.find_element_by_link_text("Set quarter info in system").click()
#         driver.find_element_by_name("Submit").click()
#         driver.find_element_by_name("Submit").click()
#         driver.find_element_by_link_text("View/Modify Waitlist").click()
#         driver.find_element_by_link_text("View/Modify Waitlist").click()
#         driver.find_element_by_css_selector("td > p > font > a").click()
#         driver.find_element_by_css_selector("td > p > font > a").click()
#         driver.find_element_by_link_text("Add/Modify/Delete MSI Supported Classes").click()
#         driver.find_element_by_link_text("Add/Modify/Delete MSI Supported Classes").click()
#         driver.find_element_by_link_text("Edit").click()
#         driver.find_element_by_link_text("Edit").click()
#         driver.find_element_by_css_selector("input[type=\"submit\"]").click()
#         driver.find_element_by_css_selector("input[type=\"submit\"]").click()
#         driver.find_element_by_link_text("Click here to return to the MSI Classes.").click()
#         driver.find_element_by_link_text("Click here to return to the MSI Classes.").click()
#         driver.find_element_by_link_text("Click here to return to the main menu.").click()
#         driver.find_element_by_link_text("Click here to return to the main menu.").click()
#         driver.find_element_by_xpath("//a[contains(text(),'Add \n                  UCSC staff to system for SID add / session browse capabilities')]").click()
#         driver.find_element_by_xpath("//a[contains(text(),'Add \n                  UCSC staff to system for SID add / session browse capabilities')]").click()
#         driver.find_element_by_id("FirstName").clear()
#         driver.find_element_by_id("FirstName").send_keys("test")
#         driver.find_element_by_id("FirstName").clear()
#         driver.find_element_by_id("FirstName").send_keys("test")
#         driver.find_element_by_id("LastName").clear()
#         driver.find_element_by_id("LastName").send_keys("tester")
#         driver.find_element_by_id("LastName").clear()
#         driver.find_element_by_id("LastName").send_keys("tester")
#         driver.find_element_by_id("Email").clear()
#         driver.find_element_by_id("Email").send_keys("testerson@ucsc.edu")
#         driver.find_element_by_id("Email").clear()
#         driver.find_element_by_id("Email").send_keys("testerson@ucsc.edu")
#         driver.find_element_by_id("Username").clear()
#         driver.find_element_by_id("Username").send_keys("testerson")
#         driver.find_element_by_id("Username").clear()
#         driver.find_element_by_id("Username").send_keys("testerson")
#         driver.find_element_by_id("Password").clear()
#         driver.find_element_by_id("Password").send_keys("test")
#         driver.find_element_by_id("Password").clear()
#         driver.find_element_by_id("Password").send_keys("test")
#         driver.find_element_by_name("Submit").click()
#         driver.find_element_by_name("Submit").click()
#         driver.find_element_by_link_text("Click here to return to the main menu.").click()
#         driver.find_element_by_link_text("Click here to return to the main menu.").click()
#         driver.find_element_by_link_text("Modify UCSC staff account").click()
#         driver.find_element_by_link_text("Modify UCSC staff account").click()
#         driver.find_element_by_name("Submit").click()
#         driver.find_element_by_name("Submit").click()
#         Select(driver.find_element_by_id("Affiliation")).select_by_visible_text("Other")
#         Select(driver.find_element_by_id("Affiliation")).select_by_visible_text("Other")
#         driver.find_element_by_name("deleteUser").click()
#         driver.find_element_by_name("deleteUser").click()
#         driver.find_element_by_name("Submit").click()
#         driver.find_element_by_name("Submit").click()
#         driver.find_element_by_link_text("Click here to return to the main menu.").click()
#         driver.find_element_by_link_text("Click here to return to the main menu.").click()
#         driver.find_element_by_link_text("Log of staff changes to MSI students").click()
#         driver.find_element_by_link_text("Log of staff changes to MSI students").click()
#         driver.find_element_by_link_text(">>").click()
#         driver.find_element_by_link_text(">>").click()
#         driver.find_element_by_link_text("Staff Member").click()
#         driver.find_element_by_link_text("Staff Member").click()
#         driver.find_element_by_link_text("Staff Member").click()
#         driver.find_element_by_link_text("Staff Member").click()
#         driver.find_element_by_link_text("Date Changed").click()
#         driver.find_element_by_link_text("Date Changed").click()
#         driver.find_element_by_link_text("Date Changed").click()
#         driver.find_element_by_link_text("Date Changed").click()
#         driver.find_element_by_link_text("Click here to return to the main menu.").click()
#         driver.find_element_by_link_text("Click here to return to the main menu.").click()
#         driver.find_element_by_link_text("View/Modify personal info").click()
#         driver.find_element_by_link_text("View/Modify personal info").click()
#         driver.find_element_by_css_selector("input[type=\"button\"]").click()
#         driver.find_element_by_css_selector("input[type=\"button\"]").click()
#         driver.find_element_by_link_text("View tutee roster").click()
#         driver.find_element_by_link_text("View tutee roster").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
