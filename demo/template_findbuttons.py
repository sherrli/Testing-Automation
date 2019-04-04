#!/usr/local/bin/python
# coding=utf-8


#--------------------------------------------------------------------
#File        : find_buttons.py
#Description : Generic helper function template to locate WebElements.
#Author      : Sherri Li
#--------------------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Note: passing in the webdriver may be costly.

# find the first input field with text type
def find_username(driver):
    # names = ["logon", "id", "SID", "username"]
    # for name in names:
    #     username = driver.find_element_by_name(name)
    #     if username is not None:
    #         return username
    # return None
    return driver.find_element_by_xpath('//input[@type="text"]')


# find the first input field with type password
def find_password(driver):
    # names = ["pass", "birthdate", "password"]
    # for name in names:
    #     password = driver.find_element_by_name(name)
    #     if password is not None:
    #         return password
    # return None
    return driver.find_element_by_xpath('//input[@type="password"]')


# Do not need to find submit button
# def find_submit(driver):
#     names = ["signinform", "submit", "Submit", "LOGIN"]
#     for name in names:
#         submit = driver.find_element_by_name(name)
#         if submit is not None:
#             return submit
#     return None
