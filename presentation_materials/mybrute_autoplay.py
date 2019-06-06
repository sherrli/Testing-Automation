#!/usr/bin/python
# -*- coding: utf-8 -*-
# This script auto-battles for you on mybrute.muxxu.com

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import unittest
import os
import logging

os.makedirs('./screenshots')
logging.basicConfig(filename='screenshots/log.log', level=logging.INFO)
                    
class AutoBattle(unittest.TestCase):
    host = "http://mybrute.muxxu.com/"
    driver = None

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(60)

    def login(self):
        driver = self.driver
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Create an account'])[1]/following::span[2]").click()
        driver.implicitly_wait(30)
        logging.info("test")
        user = input("enter your email: ")
        pw = input("enter your password: ")
        driver.find_element_by_name("login").click()
        driver.find_element_by_name("login").clear()
        driver.find_element_by_name("login").send_keys(user)
        driver.find_element_by_name("pass").click()
        driver.find_element_by_name("pass").clear()
        driver.find_element_by_name("pass").send_keys(pw)
        driver.find_element_by_id("logger").submit()

    def train(self):
        driver = self.driver
        driver.find_element_by_link_text("Train Your Brute").click()
        driver.implicitly_wait(30)
        driver.find_element_by_link_text("Fight").click()
        driver.find_element_by_link_text("chubduck").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Train Your Brute'])[1]/img[1]").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Shevii'])[3]/following::a[1]").click()


    def logout(self):
        driver = self.driver
        # mouse over to username then logout
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='My info'])[1]/following::span[1]").click()

    def test_fight(self):
        driver = self.driver
        driver.get(self.host)
        driver.save_screenshot('screenshots/mybrute.png')
        self.login()
        self.train()
        self.logout()

        self.driver.quit()



if __name__=='__main__':
    unittest.main()
